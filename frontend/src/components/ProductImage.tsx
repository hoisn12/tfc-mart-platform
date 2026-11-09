import { ImageOff } from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
export function ProductImage({src,name,large=false,onClick}:{src:string;name:string;large?:boolean;onClick?:()=>void}){const[failed,setFailed]=useState(false);useEffect(()=>setFailed(false),[src]);return <div className={cn('product-image',large&&'image-large')} onClick={onClick}>{failed||!src?<span className="image-fallback" role="img" aria-label={`${name} 이미지 없음`}><ImageOff size={large?32:18}/>{large&&<span>이미지를 불러올 수 없습니다</span>}</span>:<img src={src} alt={name} loading="lazy" onError={()=>setFailed(true)} key={src}/>}</div>;}
