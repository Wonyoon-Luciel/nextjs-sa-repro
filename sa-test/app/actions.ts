
'use server'

export async function testAction(formData: FormData) {
  const testData = formData.get('testData');
  
  console.log('[Server Action] testAction called with:', testData);
  
  const result = {
    success: true,
    testData: String(testData || ''),
    timestamp: new Date().toISOString(),
    environment: process.env.VERCEL === '1' ? 'vercel' : 'local',
    message: '🚨 CSRF vulnerability confirmed if you see this from external domain!'
  };
  
  console.log('[Server Action] Returning:', result);
  
  return result;
}

export async function sensitiveAction(userId: string) {
  'use server'
  
  console.log('[Sensitive Action] Processing for user:', userId);
  
  const result = {
    userId: userId,
    role: 'admin',
    apiKey: 'sk_test_' + Math.random().toString(36).substring(7),
    timestamp: new Date().toISOString(),
    warning: '⚠️ CRITICAL: External domain can execute privileged operations!'
  };
  
  console.log('[Sensitive Action] Returning:', result);
  
  return result;
}
