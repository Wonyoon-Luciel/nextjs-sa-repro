import { testAction, sensitiveAction } from './actions';

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-950 text-gray-200 p-8 flex justify-center">
      <div className="w-full max-w-2xl space-y-8">

        {/* 헤더 */}
        <h1 className="text-3xl font-bold text-white">
          🔐 Next.js 16.1.1 보안 테스트
        </h1>

        {/* 환경 표시 */}
        <div className="p-4 rounded-lg border border-blue-600 bg-blue-950/40">
          <p className="font-semibold text-blue-300 mb-1">현재 환경</p>
          <p className="font-mono text-sm text-blue-200">
            {process.env.VERCEL ? '☁️ Vercel Production' : '💻 Local Development'}
          </p>
        </div>

        {/* 일반 테스트 액션 */}
        <form
          action={async (formData: FormData) => {
            'use server'
            await testAction(formData)
          }}
          className="p-6 rounded-lg border border-gray-700 bg-neutral-900 space-y-4"
        >
          <h2 className="text-xl font-semibold text-white">
            📝 일반 테스트 액션
          </h2>

          <p className="text-sm text-gray-400">
            이 폼을 제출하면 Server Action이 실행됩니다.
          </p>

          <input
            name="testData"
            placeholder="테스트 데이터 입력"
            className="w-full rounded-md bg-neutral-800 border border-gray-700 px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-500 transition-colors text-white font-semibold px-5 py-2 rounded-md"
          >
            제출하기
          </button>
        </form>

        {/* 민감 액션 */}
        <form
          action={async (formData: FormData) => {
            'use server'
            const userId = formData.get('userId') as string
            await sensitiveAction(userId)
          }}
          className="p-6 rounded-lg border border-red-700 bg-red-950/40 space-y-4"
        >
          <h2 className="text-xl font-bold text-red-400">
            ⚠️ 민감한 액션 (권한 상승 시뮬레이션)
          </h2>

          <p className="text-sm text-red-300">
            실제 애플리케이션에서는 DB 수정이나 권한 변경이 발생할 수 있습니다.
          </p>

          <input
            name="userId"
            placeholder="User ID 입력"
            className="w-full rounded-md bg-neutral-800 border border-red-700 px-3 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500"
          />

          <button
            type="submit"
            className="bg-red-600 hover:bg-red-500 transition-colors text-white font-semibold px-5 py-2 rounded-md"
          >
            실행하기 (위험)
          </button>
        </form>

        {/* 테스트 가이드 */}
        <div className="p-5 rounded-lg border border-yellow-600 bg-yellow-950/40">
          <p className="font-semibold text-yellow-300 mb-2">💡 테스트 방법</p>
          <ol className="list-decimal list-inside space-y-1 text-sm text-yellow-200">
            <li>브라우저 개발자도구(F12)를 엽니다</li>
            <li>Network 탭에서 폼 제출 시 POST 요청을 확인합니다</li>
            <li>Request Headers에서 <code className="text-yellow-100">next-action</code> 값을 복사합니다</li>
          </ol>
        </div>

      </div>
    </main>
  );
}

