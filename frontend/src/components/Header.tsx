import { LogIn} from "lucide-react";
import Link from "next/link";

export function Header() {
  return (
    <header className="bg-white h-16 flex items-center px-10">
      <div className="flex justify-between w-full">
        <div className="">
          <span>Task Flow</span>
        </div>
        <div className="flex gap-5">
          <span>ユーザー名</span>
          <Link href="/login">
            
            <LogIn />
          
          </Link>
        </div>
      </div>
    </header>
  );
}
