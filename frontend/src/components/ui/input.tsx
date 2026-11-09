import { forwardRef, type InputHTMLAttributes, type SelectHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';
export const Input=forwardRef<HTMLInputElement,InputHTMLAttributes<HTMLInputElement>>(({className,...props},ref)=><input ref={ref} className={cn('input',className)} {...props}/>);
Input.displayName='Input';
export function Select({className,...props}:SelectHTMLAttributes<HTMLSelectElement>){return <select className={cn('input select',className)} {...props}/>;}
