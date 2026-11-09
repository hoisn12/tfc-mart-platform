import { useState } from 'react';
import { toast } from 'sonner';
import { usePrototype } from '@/app/PrototypeProvider';
export function useRepository(){const context=usePrototype();const[busy,setBusy]=useState(false);async function run<T>(action:()=>Promise<T>,success?:string):Promise<T|undefined>{if(busy)return;setBusy(true);try{const value=await action();await context.refresh();if(success)toast.success(success);return value;}catch(e){toast.error((e as Error).message);return undefined;}finally{setBusy(false);}}return {...context,busy,run};}
