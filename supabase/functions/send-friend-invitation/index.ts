// supabase/functions/send-friend-invitation/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

// Internationalization content
const i18n = {
  en: {
    subject: (inviterName: string) => `${inviterName} invited you to join 1000+ professionals on Jaydai! ⭐`,
    emailTitle: "Join Jaydai - AI Productivity Platform",
    headerTitle: "You're invited to Jaydai!",
    headerSubtitle: (inviterName: string) => `${inviterName} wants to share the AI productivity revolution with you`,
    mainHighlight: (inviterName: string) => `<strong>${inviterName}</strong> thinks you'll love Jaydai's AI-powered tools!`,
    mainDescription: "Join 1000+ professionals using AI templates, tracking usage, and building complex prompts in seconds.",
    ctaTitle: "Ready to 10x your productivity?",
    ctaButton: "Join Free Now! 🚀",
    benefits: {
      free: "Free forever",
      noCard: "No credit card", 
      quick: "30-second setup"
    },
    stats: "⭐⭐⭐⭐⭐ 5-star rated • 1000+ templates • 1000+ users",
    featuresTitle: "What you'll get access to:",
    features: [
      { icon: "📄", text: "Access to 1000+ premium prompt templates" },
      { icon: "✨", text: "Unlimited personal prompt templates" },
      { icon: "🗂️", text: "Unlimited personal prompt blocks" },
      { icon: "📊", text: "Advanced Data Analytics" }
    ],
    promptsTitle: "Popular prompt templates you'll discover:",
    prompts: [
      "Deck challenge",
      "Customer FAQ", 
      "KPI Business",
      "Find a restaurant",
      "Audience Analysis"
    ],
    footer: {
      invitation: (inviterName: string, friendEmail: string) => `Invitation from <strong>${inviterName}</strong> to ${friendEmail}`,
      description: "Jaydai - AI productivity platform trusted by professionals worldwide"
    }
  },
  fr: {
    subject: (inviterName: string) => `${inviterName} vous invite à rejoindre 1000+ professionnels sur Jaydai ! ⭐`,
    emailTitle: "Rejoignez Jaydai - Plateforme de Productivité IA",
    headerTitle: "Vous êtes invité(e) sur Jaydai !",
    headerSubtitle: (inviterName: string) => `${inviterName} souhaite partager la révolution IA avec vous`,
    mainHighlight: (inviterName: string) => `<strong>${inviterName}</strong> pense que vous allez adorer les outils IA de Jaydai !`,
    mainDescription: "Rejoignez 1000+ professionnels qui utilisent les modèles IA, suivent leur usage et créent des prompts complexes en secondes.",
    ctaTitle: "Prêt(e) à multiplier votre productivité par 10 ?",
    ctaButton: "Rejoindre Gratuitement ! 🚀",
    benefits: {
      free: "Gratuit à vie",
      noCard: "Aucune carte", 
      quick: "Configuration 30s"
    },
    stats: "⭐⭐⭐⭐⭐ Noté 5 étoiles • 1000+ modèles • 1000+ utilisateurs",
    featuresTitle: "Ce à quoi vous aurez accès :",
    features: [
      { icon: "📄", text: "Accès à 1000+ modèles de prompts premium" },
      { icon: "✨", text: "Modèles de prompts personnels illimités" },
      { icon: "🗂️", text: "Blocs de prompts personnels illimités" },
      { icon: "📊", text: "Analyses de données avancées" }
    ],
    promptsTitle: "Modèles de prompts populaires que vous découvrirez :",
    prompts: [
      "Challenger son deck",
      "FAQ Client",
      "KPI Business", 
      "Trouver un restaurant",
      "Analyse d'audience"
    ],
    footer: {
      invitation: (inviterName: string, friendEmail: string) => `Invitation de <strong>${inviterName}</strong> à ${friendEmail}`,
      description: "Jaydai - Plateforme de productivité IA approuvée par des professionnels du monde entier"
    }
  }
}

Deno.serve(async (req) => {
  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    const { record, locale = 'en' } = await req.json()
    
    // Validate locale
    const lang = ['en', 'fr'].includes(locale) ? locale : 'en'
    const content = i18n[lang]

    const SENDGRID_API_KEY = Deno.env.get("SENDGRID_API_KEY")!
    const FROM_EMAIL = "system@jayd.ai"
    
    // Only process friend invitations
    if (record.invitation_type === 'friend') {
      const { inviter_name, inviter_email, friend_email, id } = record

      // Send friend invitation email using SendGrid
      const emailResponse = await sendEmail({
        to: friend_email,
        from: FROM_EMAIL,
        subject: content.subject(inviter_name),
        content: createFriendInvitationEmailTemplate(inviter_name, friend_email, content),
        replyTo: inviter_email
      }, SENDGRID_API_KEY)

      if (emailResponse.ok) {
        // Update invitation status to 'sent'
        await supabase
          .from('share_invitations')
          .update({ 
            status: 'sent', 
            sent_at: new Date().toISOString(),
            metadata: { email_sent_via: 'sendgrid', locale: lang }
          })
          .eq('id', id)

        console.log(`✅ Friend invitation sent successfully to ${friend_email} in ${lang}`)
        return new Response(`Friend invitation email sent successfully in ${lang}`, { status: 200 })
      } else {
        const errorText = await emailResponse.text()
        console.error("SendGrid error:", errorText)
        
        // Update invitation status to 'failed'
        await supabase
          .from('share_invitations')
          .update({ 
            status: 'failed',
            metadata: { error: errorText, locale: lang }
          })
          .eq('id', id)

        return new Response(`SendGrid error: ${errorText}`, { status: 500 })
      }
    }

    return new Response("Function executed successfully", { status: 200 })

  } catch (error) {
    console.error('Error in friend invitation function:', error)
    return new Response(`Error: ${error.message}`, { status: 500 })
  }
})

// Helper function to send email via SendGrid
async function sendEmail({ to, from, subject, content, replyTo }, apiKey) {
  const emailData: Record<string, any> = {
    personalizations: [{ to: [{ email: to }] }],
    from: { email: from, name: "Jaydai Team" },
    subject,
    content: [{ type: "text/html", value: content }],
  }

  if (replyTo) {
    emailData.reply_to = { email: replyTo }
  }

  return await fetch("https://api.sendgrid.com/v3/mail/send", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(emailData),
  })
}

// Shorter, more engaging email template with proper image handling
function createFriendInvitationEmailTemplate(inviterName: string, friendEmail: string, content: any) {
  return `
<!DOCTYPE html>
<html lang="${content === i18n.fr ? 'fr' : 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${content.emailTitle}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f8fafc;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
            position: relative;
        }
        
        .logo {
            background: rgba(255, 255, 255, 0.15);
            width: 120px;
            height: 60px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            overflow: hidden;
        }
        
        .logo img {
            width: 100px;
            height: auto;
            max-height: 50px;
            object-fit: contain;
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .header .subtitle {
            font-size: 16px;
            opacity: 0.9;
            font-weight: 400;
        }
        
        .content {
            padding: 40px 30px;
            text-align: center;
        }
        
        .message {
            margin-bottom: 30px;
        }
        
        .message .highlight {
            font-size: 18px;
            color: #4b5563;
            margin-bottom: 12px;
            font-weight: 500;
        }
        
        .message p {
            font-size: 16px;
            color: #6b7280;
            line-height: 1.6;
        }
        
        .stats {
            font-size: 14px;
            color: #667eea;
            font-weight: 500;
            margin: 25px 0;
            padding: 15px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin: 25px 0;
            padding: 30px;
            text-align: center;
            color: white;
        }
        
        .cta-content {
            color: white;
            text-align: center;
        }
        
        .cta-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 20px;
        }
        
        .cta-button {
            display: inline-block;
            background: white;
            color: #667eea;
            text-decoration: none;
            padding: 16px 32px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 18px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.3);
        }
        
        .features-section {
            margin: 30px 0;
            padding: 25px;
            background: #f8fafc;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: #4b5563;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .feature-item:hover {
            color: #667eea;
        }
        
        .feature-icon {
            font-size: 16px;
        }
        
        .prompts-section {
            margin: 30px 0;
        }
        
        .prompts-title {
            font-size: 16px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .prompts-grid {
            display: grid;
            gap: 10px;
        }
        
        .prompt-item {
            padding: 12px 15px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid #667eea;
            font-size: 14px;
            color: #4b5563;
            font-weight: 500;
        }
        
        .benefits {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 13px;
            opacity: 0.9;
        }
        
        .benefit::before {
            content: '✓';
            margin-right: 5px;
            color: #10b981;
            font-weight: bold;
        }
        
        .footer {
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            font-size: 14px;
            color: #9ca3af;
        }
        
        .footer p {
            margin-bottom: 10px;
        }
        
        .footer a {
            color: #667eea;
            text-decoration: none;
        }
        
        @media (max-width: 600px) {
            body { padding: 10px; }
            .container { border-radius: 12px; }
            .header, .content, .footer { padding: 25px 20px; }
            .cta-section { padding: 25px 20px; }
            .features-section { padding: 20px 15px; }
            .features-grid { grid-template-columns: 1fr; gap: 10px; }
            .benefits { flex-direction: column; gap: 8px; }
            .header h1 { font-size: 24px; }
            .cta-title { font-size: 20px; }
            .cta-button { font-size: 16px; padding: 14px 28px; }
            .logo { width: 100px; height: 50px; }
            .logo img { width: 80px; max-height: 40px; }
        }

        @media (prefers-color-scheme: dark) {
            body { background: #1f2937; }
            .container { background: #111827; }
            .content { color: #f9fafb; }
            .message .highlight { color: #d1d5db; }
            .message p { color: #9ca3af; }
            .stats { background: #374151; color: #93c5fd; border-color: #3b82f6; }
            .features-section { background: #374151; border-color: #3b82f6; }
            .feature-item { color: #d1d5db; }
            .feature-item:hover { color: #93c5fd; }
            .prompts-title { color: #f9fafb; }
            .prompt-item { background: #374151; color: #d1d5db; border-color: #3b82f6; }
            .footer { background: #1f2937; color: #6b7280; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <img src="https://vetoswvwgsebhxetqppa.supabase.co/storage/v1/object/public/images/organizations/jaydai_org_logo.png" alt="Jaydai Logo" />
            </div>
            <h1>${content.headerTitle}</h1>
            <p class="subtitle">${content.headerSubtitle(inviterName)}</p>
        </div>
        
        <div class="content">
            <div class="message">
                <p class="highlight">${content.mainHighlight(inviterName)}</p>
                <p>${content.mainDescription}</p>
            </div>
            
            <div class="stats">${content.stats}</div>
            
            <div class="cta-section">
                <div class="cta-content">
                    <h2 class="cta-title">${content.ctaTitle}</h2>
                    <a href="https://jayd.ai?ref=${encodeURIComponent(inviterName)}&invited_by=${encodeURIComponent(friendEmail)}" class="cta-button">
                        ${content.ctaButton}
                    </a>
                    <div class="benefits">
                        <div class="benefit">${content.benefits.free}</div>
                        <div class="benefit">${content.benefits.noCard}</div>
                        <div class="benefit">${content.benefits.quick}</div>
                    </div>
                </div>
            </div>

            <!-- Features Section -->
            <div class="features-section">
                <h3 style="font-size: 16px; font-weight: 600; color: #1f2937; margin-bottom: 15px; text-align: center;">
                    ${content.featuresTitle}
                </h3>
                <div class="features-grid">
                    ${content.features.map(feature => `
                        <a href="https://www.jayd.ai/${content === i18n.fr ? 'fr' : 'en'}#features" class="feature-item">
                            <span class="feature-icon">${feature.icon}</span>
                            <span>${feature.text}</span>
                        </a>
                    `).join('')}
                </div>
            </div>

            <!-- Prompts Examples Section -->
            <div class="prompts-section">
                <h3 class="prompts-title">${content.promptsTitle}</h3>
                <div class="prompts-grid">
                    ${content.prompts.map(prompt => `
                        <div class="prompt-item">${prompt}</div>
                    `).join('')}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>${content.footer.invitation(inviterName, friendEmail)}</p>
            <p>${content.footer.description}</p>
            <p><a href="https://jayd.ai">jayd.ai</a></p>
        </div>
    </div>
</body>
</html>
`
}