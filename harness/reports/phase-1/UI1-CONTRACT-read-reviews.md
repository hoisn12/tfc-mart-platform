# 구현자 계약 읽기 검토 원문

## frontend

UI1 frontend 계약 읽기 검토 PASS. behavior/openapi SHA-256가 전달값과 일치. 6 경로·상품 모델/정수금액·soft delete·version/부분실패·Query snapshot·저장소 손상/쓰기실패·이미지 READY 전 유지·SMS UNKNOWN 경계 모두 frontend 구현 가능. 실제 메서드명 조정 허용으로 불필요한 API 구현 없이 AppRepository를 교체점으로 둘 수 있음. 문서 수정 없음, 실행 테스트는 아직 NOT_RUN. 독립 검토와 메인 동결/정확 파일 잠금 배정 대기.

## backend

판정: **PASS — 프론트엔드 데모 구현을 차단할 계약 모순 없음.**

- Repository/local adapter와 미래 REST 경계가 분리돼 있습니다.
- 원 단위 안전 정수, 문자열 바코드, version 충돌·부분 실패가 정의돼 있습니다.
- 마트 선택을 실제 서버 인가로 오인하지 않도록 한계를 명시했습니다.
- 문자 접수·전달·UNKNOWN을 구분하며 UNKNOWN 재발송을 금지합니다.
- 이미지 READY 이전에는 기존 대표를 유지합니다.

두 계약의 SHA-256이 전달값과 일치했습니다. 읽기·해시 확인 명령은 모두 종료 0입니다. 파일 수정·설치·실행 테스트·백엔드 구현은 수행하지 않았습니다.

OpenAPI는 미래 연결점 초안입니다. 실제 서버 구현 전에는 인증·인가·멱등성 및 이미지 업로드 계약을 별도로 확정해야 합니다. 기존 전체 시스템 gate는 BLOCKED 상태를 유지합니다.

## reliability

안전 계약 읽기 검토 PASS. 구현 차단 모순은 발견하지 못했습니다. 실행 검증·운영 검증은 NOT_RUN입니다. 외부 SMS/AWS/DB 호출/실제 번호 제외, UNKNOWN 재발송 금지, LocalStorage 손상 자동 덮어쓰기 금지/실패 안내/앱 키 초기화, 이미지 5MiB/디코딩/READY 전 기존 대표 유지/fallback 복구, UI 권한 한계와 전체 gate 차단 구분을 확인. cat/shasum 종료0 및 전달 해시 일치. 저장소 수정/설치/재위임 없음. 임시 읽기 사본 /private/tmp/tfc-ui1-reliability-readonly-input.txt 생성.
