import type { ReactNode } from 'react';
import { ArrowUpRight, Inbox, SearchX, LoaderCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from './ui/button';
export function PageHeader({eyebrow,title,description,actions}:{eyebrow?:string;title:string;description:string;actions?:ReactNode}){return <div className="page-header"><div>{eyebrow&&<div className="eyebrow">{eyebrow}</div>}<h1>{title}</h1><p>{description}</p></div><div className="page-actions">{actions}</div></div>;}
export function StatCard({label,value,detail,icon,tone='green'}:{label:string;value:ReactNode;detail?:string;icon:ReactNode;tone?:string}){return <div className="stat-card"><div className="stat-top"><span>{label}</span><span className={cn('stat-icon',`stat-icon-${tone}`)}>{icon}</span></div><strong>{value}</strong><div className="stat-detail"><ArrowUpRight size={13}/>{detail??'데모 데이터 기준'}</div></div>;}
export function EmptyState({title='검색 결과가 없습니다',description='검색어나 필터를 변경해 다시 확인해 주세요.',action}:{title?:string;description?:string;action?:ReactNode}){return <div className="empty-state"><div className="empty-icon"><SearchX size={25}/></div><h3>{title}</h3><p>{description}</p>{action}</div>;}
export function LoadingState(){return <div className="empty-state" role="status"><LoaderCircle className="spin" size={26}/><h3>데이터를 불러오는 중입니다</h3><p>데모 작업공간을 준비하고 있습니다.</p></div>;}
export function SectionTitle({title,description,action}:{title:string;description?:string;action?:ReactNode}){return <div className="section-title"><div><h2>{title}</h2>{description&&<p>{description}</p>}</div>{action}</div>;}
export function DemoNote({children}:{children?:ReactNode}){return <div className="demo-note"><Inbox size={14}/>{children??'이 화면의 모든 정보는 합성 샘플 데이터입니다.'}</div>;}
export function ErrorState({message,onRetry}:{message:string;onRetry:()=>void}){return <EmptyState title="데이터를 불러오지 못했습니다" description={message} action={<Button onClick={onRetry}>다시 시도</Button>}/>;}
