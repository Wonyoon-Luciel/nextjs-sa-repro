import { testAction, sensitiveAction } from './actions';

export default function Home() {
  return (
    <main className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">
        🔐 Next.js 16.1.1 보안 테스트
      </h1>

      <div className="mb-8 p-4 bg-blue-100 border-2 border-blue-400 rounded-lg">
        <p className="font-semibold text-blue-900">현재 환경:</p>
        <p className="font-mono text-sm mt-2 text-blue-800">
          {process.env.VERCEL ? '☁️ Vercel Production' : '💻 Local Development'}
        </p>
      </div>

      {/* 일반 테스트 액션 */}
      <form
        action={async (formData: FormData) => {
          'use server'
          await testAction(formData)
        }}
        className="mb-8 p-6 border-2 rounded-lg bg-gray-50"
      >
        <h2 className="text-xl font-semibold mb-3 test-gray-900">📝 일반 테스트 액션</h2>
        <p className="text-sm text-gray-800 mb-4">
          이 폼을 제출하면 Server Action이 실행됩니다.
        </p>
        <input
          name="testData"
          placeholder="테스트 데이터 입력"
          className="border-2 p-3 w-full mb-3 rounded"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 font-semibold"
        >
          제출하기
        </button>
      </form>

      {/* 민감한 액션 */}
      <form
        action={async (formData: FormData) => {
          'use server'
          const userId = formData.get('userId') as string
          await sensitiveAction(userId)
        }}
        className="p-6 border-2 border-red-300 rounded-lg bg-red-50"
      >
        <h2 className="text-xl font-bold mb-3 text-red-800">
          ⚠️ 민감한 액션 (권한 상승 시뮬레이션)
        </h2>
        <p className="text-sm text-red-700 mb-4">
          실제 앱에서는 이런 액션이 DB를 수정하거나 권한을 변경할 수 있습니다.
        </p>
        <input
          name="userId"
          placeholder="User ID 입력"
          className="border-2 p-3 w-full mb-3 rounded"
        />
        <button
          type="submit"
          className="bg-red-500 text-white px-6 py-3 rounded-lg hover:bg-red-600 font-semibold"
        >
          실행하기 (위험!)
        </button>
      </form>

      <div className="mt-8 p-4 bg-yellow-100 border-2 border-yellow-400 rounded-lg">
        <p className="text-sm font-semibold">💡 테스트 방법:</p>
        <ol className="text-sm mt-2 space-y-1 list-decimal list-inside test-yellow-900">
          <li>브라우저 개발자도구(F12)를 열고 Network 탭을 확인하세요</li>
          <li>폼을 제출하고 POST 요청을 찾으세요</li>
          <li>요청 헤더에서 <code>next-action</code> 값을 복사하세요</li>
        </ol>
      </div>
    </main>
  );
}

