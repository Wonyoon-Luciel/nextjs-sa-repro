'use server'

// 기본 테스트용 액션
export async function testAction(formData: FormData) {
  const data = Object.fromEntries(formData);
  console.log('[Server Action] Received data:', data);
  
  return { 
    success: true, 
    data,
    timestamp: new Date().toISOString(),
    environment: process.env.VERCEL ? 'vercel' : 'local',
    message: '이 데이터가 외부에서 접근되면 취약점입니다!'
  };
}

// 민감한 작업을 시뮬레이션 (실제로는 DB 변경 등을 할 수 있음)
export async function sensitiveAction(userId: string) {
  'use server'
  
  console.log('[Sensitive Action] Processing for user:', userId);
  
  // 실제 앱이라면 여기서 DB를 변경하거나 권한을 상승시킬 수 있음
  return {
    userId,
    role: 'admin', // ⚠️ 권한 상승 시뮬레이션
    apiKey: 'sk_test_' + Math.random().toString(36),
    timestamp: new Date().toISOString(),
    warning: '⚠️ 이 액션이 외부에서 호출되면 심각한 보안 문제!'
  };
}
