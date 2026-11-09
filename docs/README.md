# Phase 0 설계 문서

기준일: 2026-11-05. 기본 명세: [PRD](../MART_RENEWAL_PRD.md), [Coding Agent Prompt](../MART_CODING_AGENT_PROMPT.md). 이번 사용자 지시가 우선하며 **Phase 0만 수행**한다. 구현, 의존성 설치, SQL 실행, 인프라 생성, 실발송은 범위 밖이다.

| 문서 | 내용 |
|---|---|
| [현황 분석](project-analysis.md) | 자료 범위, 프로젝트 및 레거시 분석 한계 |
| [기능·화면 대응표](legacy-feature-matrix.md) | 기능별 근거, 신규 화면, 유지/변경/보류 |
| [요구사항](requirements.md) | 기능 요구사항, 권한, UI 및 작업 상태 |
| [아키텍처](architecture.md) | 모듈·포트·트랜잭션, 구성도·시퀀스·ADR |
| [데이터 모델](data-model.md) | ERD, 후보 테이블·제약·인덱스 |
| [API 초안](api-spec.md) | API 계약, 요청/응답, 동시성·멱등성 |
| [가정·미확인·위험](assumptions.md) | 확인 질문, 영향, 검증 방법, 위험 관리 |
| [개발·전환 계획](migration-plan.md) | Phase별 범위·인수 기준, cutover/rollback |
| [검증 계획](test-plan.md) | 기능·격리·장애·복구 시나리오 |
| [진행 기록](PROGRESS.md) | 이번 작업 및 검증 결과, 다음 단계 |

문서의 ‘제안’은 신규 시스템 설계안이고 레거시 사실이 아니다. ‘미확인’은 자료나 실행 증거가 없는 상태다. Phase 0 문서 작성 완료와 Discovery 승인 완료를 구분한다. 상세 OpenAPI YAML, Flyway SQL, 실행 가능한 runbook은 해당 구현 단계에서 작성하며 현재 문서는 그 계약과 인수 조건의 초안이다.
