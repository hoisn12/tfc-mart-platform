import { Route, Routes, Link } from 'react-router-dom';
import { PrototypeProvider } from './PrototypeProvider';
import { AppShell } from './AppShell';
import { DashboardPage } from '@/features/dashboard/DashboardPage';
import { ProductsPage } from '@/features/products/ProductsPage';
import { MessagingPage } from '@/features/messaging/MessagingPage';
import { ImagesPage } from '@/features/images/ImagesPage';
import { MembersPage } from '@/features/members/MembersPage';
import { SettingsPage } from '@/features/settings/SettingsPage';
import { EmptyState } from '@/components/shared';
export function App(){return <PrototypeProvider><AppShell><Routes><Route path="/" element={<DashboardPage/>}/><Route path="/products" element={<ProductsPage/>}/><Route path="/messaging" element={<MessagingPage/>}/><Route path="/images" element={<ImagesPage/>}/><Route path="/members" element={<MembersPage/>}/><Route path="/settings" element={<SettingsPage/>}/><Route path="*" element={<EmptyState title="페이지를 찾을 수 없습니다" description="메뉴를 선택하거나 대시보드로 돌아가 주세요." action={<Link className="btn btn-primary" to="/">대시보드로 이동</Link>}/>}/></Routes></AppShell></PrototypeProvider>;}
