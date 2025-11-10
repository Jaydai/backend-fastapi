import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const SENDGRID_API_KEY = Deno.env.get('SENDGRID_API_KEY')
const FRONTEND_URL = Deno.env.get('FRONTEND_URL') || 'http://localhost:3000'

interface InvitationEmailRequest {
  to_email: string
  inviter_name: string
  organization_name: string
  invitation_id: string
  role: string
  locale?: string
}

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, accept-language',
}

// Internationalization content for organization invitations
const i18n = {
  en: {
    subject: (inviterName: string, orgName: string) => `${inviterName} invited you to join ${orgName}`,
    title: "🎉 You're Invited!",
    greeting: "Hi there,",
    invitationText: (inviterName: string, orgName: string) => `<strong>${inviterName}</strong> has invited you to join <span class="org-name">${orgName}</span> on Jaydai.`,
    detailsTitle: {
      organization: "Organization:",
      role: "Role:",
      invitedBy: "Invited by:"
    },
    ctaText: "Click the button below to accept your invitation and create your account:",
    buttonText: "Accept Invitation & Join",
    linkText: "Or copy and paste this link into your browser:",
    expiryText: "This invitation link will expire in 7 days. If you didn't expect this invitation, you can safely ignore this email.",
    footer: {
      sentBy: "Sent by",
      needHelp: "Need help?",
      contactSupport: "Contact Support"
    }
  },
  fr: {
    subject: (inviterName: string, orgName: string) => `${inviterName} vous invite à rejoindre ${orgName}`,
    title: "🎉 Vous êtes invité(e) !",
    greeting: "Bonjour,",
    invitationText: (inviterName: string, orgName: string) => `<strong>${inviterName}</strong> vous a invité(e) à rejoindre <span class="org-name">${orgName}</span> sur Jaydai.`,
    detailsTitle: {
      organization: "Organisation :",
      role: "Rôle :",
      invitedBy: "Invité(e) par :"
    },
    ctaText: "Cliquez sur le bouton ci-dessous pour accepter votre invitation et créer votre compte :",
    buttonText: "Accepter l'invitation et rejoindre",
    linkText: "Ou copiez et collez ce lien dans votre navigateur :",
    expiryText: "Ce lien d'invitation expirera dans 7 jours. Si vous ne vous attendiez pas à cette invitation, vous pouvez ignorer cet e-mail en toute sécurité.",
    footer: {
      sentBy: "Envoyé par",
      needHelp: "Besoin d'aide ?",
      contactSupport: "Contacter le support"
    }
  }
}

function getEmailContent(
  inviterName: string,
  organizationName: string,
  invitationUrl: string,
  role: string,
  locale: string
) {
  const lang = locale.startsWith('fr') ? 'fr' : 'en'
  const content = i18n[lang]
  const roleCapitalized = role.charAt(0).toUpperCase() + role.slice(1)

  const htmlContent = `
<!DOCTYPE html>
<html lang="${lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${content.subject(inviterName, organizationName)}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
      background-color: #f5f5f5;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }
    .email-wrapper {
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 40px 20px;
      text-align: center;
      color: white;
    }
    .header h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 600;
    }
    .content {
      padding: 40px 30px;
    }
    .content p {
      margin: 0 0 16px 0;
      font-size: 16px;
    }
    .org-name {
      font-weight: 600;
      color: #667eea;
    }
    .button-container {
      text-align: center;
      margin: 32px 0;
    }
    .button {
      display: inline-block;
      padding: 14px 32px;
      background: white !important;
      color: #667eea !important;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 16px;
      transition: transform 0.2s;
      border: 2px solid #667eea;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    .details {
      background-color: #f8f9fa;
      border-left: 4px solid #667eea;
      padding: 16px;
      margin: 24px 0;
      border-radius: 4px;
    }
    .details p {
      margin: 8px 0;
      font-size: 14px;
    }
    .footer {
      padding: 20px 30px;
      background-color: #f8f9fa;
      text-align: center;
      font-size: 14px;
      color: #666;
    }
    .footer a {
      color: #667eea;
      text-decoration: none;
    }
    .divider {
      height: 1px;
      background-color: #e0e0e0;
      margin: 24px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="email-wrapper">
      <div class="header">
        <h1>${content.title}</h1>
      </div>

      <div class="content">
        <p>${content.greeting}</p>

        <p>${content.invitationText(inviterName, organizationName)}</p>

        <div class="details">
          <p><strong>${content.detailsTitle.organization}</strong> ${organizationName}</p>
          <p><strong>${content.detailsTitle.role}</strong> ${roleCapitalized}</p>
          <p><strong>${content.detailsTitle.invitedBy}</strong> ${inviterName}</p>
        </div>

        <p>${content.ctaText}</p>

        <div class="button-container">
          <a href="${invitationUrl}" class="button">${content.buttonText}</a>
        </div>

        <div class="divider"></div>

        <p style="font-size: 14px; color: #666;">
          ${content.linkText}<br>
          <a href="${invitationUrl}" style="color: #667eea; word-break: break-all;">${invitationUrl}</a>
        </p>

        <p style="font-size: 14px; color: #666; margin-top: 24px;">
          ${content.expiryText}
        </p>
      </div>

      <div class="footer">
        <p>
          ${content.footer.sentBy} <a href="${FRONTEND_URL}">Jaydai</a><br>
          ${content.footer.needHelp} <a href="${FRONTEND_URL}/support">${content.footer.contactSupport}</a>
        </p>
      </div>
    </div>
  </div>
</body>
</html>
  `

  const textContent = `
${content.title}

${inviterName} ${lang === 'fr' ? 'vous a invité(e) à rejoindre' : 'has invited you to join'} ${organizationName} ${lang === 'fr' ? 'sur' : 'on'} Jaydai.

${content.detailsTitle.organization} ${organizationName}
${content.detailsTitle.role} ${roleCapitalized}
${content.detailsTitle.invitedBy} ${inviterName}

${lang === 'fr' ? 'Cliquez sur le lien ci-dessous pour accepter votre invitation et créer votre compte' : 'Click the link below to accept your invitation and create your account'}:
${invitationUrl}

${content.expiryText}

${content.footer.sentBy} Jaydai
${content.footer.needHelp} ${lang === 'fr' ? 'Visitez' : 'Visit'} ${FRONTEND_URL}/support
  `

  return { htmlContent, textContent, subject: content.subject(inviterName, organizationName) }
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Parse request body
    const { to_email, inviter_name, organization_name, invitation_id, role }: InvitationEmailRequest = await req.json()

    // Always use French for organization invitations
    const finalLocale = 'fr'

    // Validate required fields
    if (!to_email || !inviter_name || !organization_name || !invitation_id) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // Create invitation URL
    const invitationUrl = `${FRONTEND_URL}/invite/${invitation_id}`

    // Get email content based on locale
    const { htmlContent, textContent, subject } = getEmailContent(
      inviter_name,
      organization_name,
      invitationUrl,
      role || 'member',
      finalLocale
    )

    // Send email using SendGrid
    const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SENDGRID_API_KEY}`,
      },
      body: JSON.stringify({
        personalizations: [{
          to: [{ email: to_email }],
          subject
        }],
        from: {
          email: 'invitations@jayd.ai',
          name: 'Jaydai'
        },
        content: [
          {
            type: 'text/plain',
            value: textContent
          },
          {
            type: 'text/html',
            value: htmlContent
          }
        ]
      }),
    })

    if (!res.ok) {
      const errorText = await res.text()
      console.error('SendGrid API error:', errorText)
      return new Response(
        JSON.stringify({ error: 'Failed to send email', details: errorText }),
        { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    console.log(`Email sent successfully via SendGrid in ${finalLocale}`)

    return new Response(
      JSON.stringify({ success: true, locale: finalLocale }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('Error in send-invitation-email function:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
