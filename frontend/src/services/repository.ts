import type { AppSnapshot, BulkResult, DemoMessageRequest, DemoSettings, ImageAsset, Message, Preferences, Product, ProductInput, StatusPatch, VersionRef } from '@/types';
export class ServiceError extends Error { constructor(public code: 'VALIDATION' | 'NOT_FOUND' | 'CONFLICT' | 'STORAGE_UNAVAILABLE' | 'STORAGE_CORRUPT', message: string) { super(message); this.name = 'ServiceError'; } }
export interface AppRepository {
  getState(): Promise<AppSnapshot>;
  saveProduct(input: ProductInput, existing?: VersionRef): Promise<Product>;
  archiveProducts(items: VersionRef[]): Promise<BulkResult>;
  bulkProducts(items: VersionRef[], changes: StatusPatch): Promise<BulkResult>;
  requestMessage(input: DemoMessageRequest): Promise<Message>;
  advanceMessage(id: string): Promise<Message>;
  previewImage(file: File): Promise<string>;
  uploadImage(file: File, productId: string): Promise<ImageAsset>;
  retryImage(id: string): Promise<ImageAsset>;
  updateSettings(input: DemoSettings): Promise<DemoSettings>;
  reset(): Promise<AppSnapshot>;
  getPreferences(): Preferences;
  setPreferences(patch: Partial<Preferences>): void;
}
