import type { HTMLAttributes, TableHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';
export function Table({className,...props}:TableHTMLAttributes<HTMLTableElement>){return <div className="table-scroll"><table className={cn('data-table',className)} {...props}/></div>;}
export function TableHeader(props:HTMLAttributes<HTMLTableSectionElement>){return <thead {...props}/>;}
export function TableBody(props:HTMLAttributes<HTMLTableSectionElement>){return <tbody {...props}/>;}
