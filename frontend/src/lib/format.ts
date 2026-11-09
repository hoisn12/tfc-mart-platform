export const won = (n: number) => new Intl.NumberFormat('ko-KR').format(n) + '원';
export const number = (n: number) => new Intl.NumberFormat('ko-KR').format(n);
export const date = (s: string) => new Intl.DateTimeFormat('ko-KR', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(s));
export const saleLabel = { ON_SALE: '판매 중', STOPPED: '판매 중지' };
export const stockLabel = { IN_STOCK: '재고 있음', LOW_STOCK: '재고 부족', OUT_OF_STOCK: '품절' };
export const messageLabel = { PENDING: '요청 접수', PROCESSING: '처리 중', ACCEPTED: '발송사 접수', DELIVERED: '전달 성공', FAILED: '실패', UNKNOWN: '결과 미확정' };
