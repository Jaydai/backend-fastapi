// supabase/functions/send-internal-notifications/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

console.log("Internal Notifications Function Started!")

Deno.serve(async (req) => {
  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SECRET_KEY')!
    )

    const { record } = await req.json()

    const SENDGRID_API_KEY = Deno.env.get("SENDGRID_API_KEY")!
    const FROM_EMAIL = "system@jayd.ai"
    const CONTACT_EMAIL = "contact@jayd.ai"
    
    // Process team invitation and referral program requests
    if (record.invitation_type === 'team' || record.invitation_type === 'referral') {
      const { inviter_name, inviter_email, invitation_type, id, user_id } = record

      // Get user metadata to check for phone number
      let phone_number = null
      try {
        const userResponse = await supabase.auth.admin.get_user_by_id(user_id)
        if (userResponse?.user?.user_metadata) {
          phone_number = userResponse.user.user_metadata.phone_number || 
                        userResponse.user.user_metadata.phone ||
                        userResponse.user.user_metadata.phoneNumber ||
                        null
        }
      } catch (error) {
        console.log("Could not fetch user metadata:", error)
      }

      const emailTemplate = createSimpleNotificationTemplate(
        inviter_name, 
        inviter_email, 
        phone_number, 
        invitation_type
      )
      
      const subject = invitation_type === 'team' 
        ? `🏢 Team Invitation Request from ${inviter_name}`
        : `🎁 Referral Program Request from ${inviter_name}`

      // Send internal notification email using SendGrid
      const emailResponse = await sendEmail({
        to: CONTACT_EMAIL,
        from: FROM_EMAIL,
        subject: subject,
        content: emailTemplate,
        replyTo: inviter_email
      }, SENDGRID_API_KEY)

      if (emailResponse.ok) {
        // Update invitation status to 'sent'
        await supabase
          .from('share_invitations')
          .update({ 
            status: 'sent', 
            sent_at: new Date().toISOString(),
            metadata: { 
              email_sent_via: 'sendgrid',
              notification_sent: true,
              phone_number: phone_number 
            }
          })
          .eq('id', id)

        console.log(`✅ ${invitation_type} notification sent successfully for user:`, inviter_email)
        return new Response(`${invitation_type} notification sent successfully`, { status: 200 })
      } else {
        const errorText = await emailResponse.text()
        console.error("SendGrid error:", errorText)
        
        // Update invitation status to 'failed'
        await supabase
          .from('share_invitations')
          .update({ 
            status: 'failed',
            metadata: { error: errorText }
          })
          .eq('id', id)

        return new Response(`SendGrid error: ${errorText}`, { status: 500 })
      }
    }

    return new Response("Function executed successfully", { status: 200 })

  } catch (error) {
    console.error('Error in internal notifications function:', error)
    return new Response(`Error: ${error.message}`, { status: 500 })
  }
})

// Helper function to send email via SendGrid
async function sendEmail({ to, from, subject, content, replyTo }, apiKey) {
  const emailData = {
    personalizations: [{ to: [{ email: to }] }],
    from: { email: from, name: "Jaydai System" },
    subject: subject,
    content: [{ type: "text/html", value: content }],
  }

  // Add reply-to if provided
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

// Simple email template with just the essential information
function createSimpleNotificationTemplate(
  userName: string, 
  userEmail: string, 
  phoneNumber: string | null, 
  invitationType: string
) {
  const typeIcon = invitationType === 'team' ? '🏢' : '🎁'
  const typeLabel = invitationType === 'team' ? 'Team Invitation' : 'Referral Program'
  
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${typeLabel} Request</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #374151;
            background-color: #f8fafc;
            margin: 0;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            color: white;
            text-align: center;
        }
        
        .header h1 {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
        }
        
        .content {
            padding: 30px;
        }
        
        .user-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .info-row:last-child {
            margin-bottom: 0;
            border-bottom: none;
        }
        
        .label {
            font-weight: 600;
            color: #374151;
        }
        
        .value {
            color: #6b7280;
            text-align: right;
        }
        
        .email-value {
            color: #667eea;
            font-weight: 500;
        }
        
        .phone-value {
            color: #059669;
            font-weight: 500;
        }
        
        .type-badge {
            display: inline-block;
            background: ${invitationType === 'team' ? '#dcfce7' : '#fef3c7'};
            color: ${invitationType === 'team' ? '#166534' : '#92400e'};
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .footer {
            background: #f9fafb;
            padding: 20px 30px;
            color: #9ca3af;
            font-size: 14px;
            text-align: center;
        }

        @media (prefers-color-scheme: dark) {
            body { background-color: #1f2937; }
            .container { background: #111827; }
            .content { color: #f9fafb; }
            .user-card { background: #374151; border-left-color: #60a5fa; }
            .label { color: #f3f4f6; }
            .value { color: #d1d5db; }
            .footer { background: #1f2937; color: #6b7280; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>${typeIcon} ${typeLabel} Request</h1>
        </div>
        
        <div class="content">
            <div class="user-card">
                <div class="info-row">
                    <span class="label">Name:</span>
                    <span class="value">${userName}</span>
                </div>
                <div class="info-row">
                    <span class="label">Email:</span>
                    <span class="value email-value">${userEmail}</span>
                </div>
                ${phoneNumber ? `
                <div class="info-row">
                    <span class="label">Phone:</span>
                    <span class="value phone-value">${phoneNumber}</span>
                </div>
                ` : ''}
                <div class="info-row">
                    <span class="label">Request Type:</span>
                    <span class="value">
                        <span class="type-badge">${typeLabel}</span>
                    </span>
                </div>
                <div class="info-row">
                    <span class="label">Date:</span>
                    <span class="value">${new Date().toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'short', 
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    })}</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Jaydai Internal Notification System</p>
        </div>
    </div>
</body>
</html>
`
}