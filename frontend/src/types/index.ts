export type SaleStatus = 'ON_SALE' | 'STOPPED';
export type StockStatus = 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK';
export interface Mart { id: string; name: string; branch: string }
export interface Product { id: string; code: string; barcode: string; name: string; martId: string; category: string; brand: string; specification: string; price: number; discountPrice: number | null; minOrder: number; maxOrder: number; saleStatus: SaleStatus; visible: boolean; stockStatus: StockStatus; imageId?: string; imageUrl: string; version: number; updatedAt: string; deletedAt?: string }
export type ProductInput = Omit<Product, 'id' | 'version' | 'updatedAt' | 'deletedAt'>;
export type StatusPatch = Partial<Pick<Product, 'saleStatus' | 'visible' | 'stockStatus'>>;
export interface VersionRef { id: string; version: number }
export interface BulkResult { succeeded: string[]; failed: { id: string; code: string }[] }
export type MessageStatus = 'PENDING' | 'PROCESSING' | 'ACCEPTED' | 'DELIVERED' | 'FAILED' | 'UNKNOWN';
export interface Message { id: string; martId: string; title: string; body: string; type: 'SMS' | 'LMS'; audienceId: string; total: number; succeeded: number; failed: number; unknown: number; pending: number; status: MessageStatus; scheduledAt: string | null; createdAt: string }
export type DemoMessageRequest = Pick<Message, 'martId' | 'title' | 'body' | 'type' | 'audienceId' | 'scheduledAt'>;
export interface ImageAsset { id: string; productId: string; martId: string; name: string; mimeType: string; bytes: number; url: string; status: 'PROCESSING' | 'READY' | 'FAILED'; createdAt: string; failure?: string }
export interface Member { id: string; martId: string; name: string; status: 'ACTIVE' | 'DORMANT' | 'WITHDRAWN'; maskedContact: string; joinedAt: string; orders: number; grade: string }
export interface DemoSettings { martId: string; name: string; address: string; description: string; minOrderAmount: number; lowStockAlert: boolean; orderNotification: boolean }
export interface Audit { id: string; martId: string; productId: string; productName: string; action: string; at: string; actor: string }
export interface AppSnapshot { schemaVersion: 1; marts: Mart[]; products: Product[]; messages: Message[]; images: ImageAsset[]; members: Member[]; settings: DemoSettings[]; audit: Audit[]; admins: {id:string;name:string;role:string;martId:string;status:string}[]; metrics: { date:string; orders:number; revenue:number; weekRevenue:number; monthRevenue:number; chartWeek:number[]; chartMonth:number[]; previous:number[]; weekLabels:string[];monthLabels:string[] } }
export interface Preferences { martId: string; collapsed: boolean; columns: Record<string, boolean> }
