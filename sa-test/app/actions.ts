'use server'

// 기본 테스트용 액션
export async function testAction(formData: FormData) {
  const data = Object.fromEntries(formData);
  console.log('[Server Action] Received data:', data);
  // ⚠️ form action에서는 return 절대 금지
}

// 민감한 작업 시뮬레이션 (권한 상승 등)
export async function sensitiveAction(userId: string) {
  console.log('[Sensitive Action] Processing for user:', userId);
  // ⚠️ 마찬가지로 return 제거
}

