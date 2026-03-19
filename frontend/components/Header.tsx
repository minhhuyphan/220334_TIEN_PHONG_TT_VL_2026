import React from 'react';
import { User } from '../types';
import { Coins, Menu } from 'lucide-react';

interface HeaderProps {
  user: User;
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, onMenuClick }) => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-8 sticky top-0 z-10">
      <div className="flex items-center gap-3">
        <button 
          onClick={onMenuClick}
          className="p-2 -ml-2 text-slate-600 md:hidden hover:bg-slate-100 rounded-lg transition-colors"
        >
          <Menu className="h-6 w-6" />
        </button>
        <div className="md:hidden flex items-center gap-2">
           <img src="/logo.png" alt="Logo" className="h-8 w-8 object-contain" />
           <span className="font-bold text-indigo-600 text-sm">AutoBanner</span>
        </div>
      </div>

      <div className="flex items-center gap-3 md:gap-6">
        <div className="flex items-center gap-2 bg-indigo-50 px-3 py-1.5 rounded-full border border-indigo-100 shadow-sm">
          <Coins className="h-4 w-4 text-indigo-600" />
          <span className="text-[10px] md:text-sm font-bold text-indigo-700">{user.tokens.toLocaleString()} Credits</span>
        </div>
        

        <div className="flex items-center gap-2 md:gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-semibold text-slate-900 line-clamp-1">{user.full_name}</p>
            <p className="text-xs text-slate-500 line-clamp-1">{user.email}</p>
          </div>
          <img 
            src={user.avatar || `https://picsum.photos/seed/${user.id}/40/40`} 
            alt={user.full_name} 
            className="h-8 w-8 md:h-10 md:w-10 rounded-full border-2 border-indigo-100 object-cover"
          />
        </div>
      </div>
    </header>
  );
};

export default Header;
