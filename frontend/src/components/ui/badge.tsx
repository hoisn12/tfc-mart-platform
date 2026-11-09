import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';
export function Badge({children,tone='neutral',dot=true}: {children:ReactNode;tone?:'green'|'amber'|'red'|'blue'|'neutral';dot?:boolean}){return <span className={cn('badge',`badge-${tone}`)}>{dot&&<span className="badge-dot"/>}{children}</span>;}
