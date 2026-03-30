"use client";

import Link from "next/link";
import { ComponentProps, ReactNode } from "react";

interface CardInicialProps extends Omit<ComponentProps<"div">, "title"> {
  sigla: string;
  descricao?: string;
  icone: ReactNode; 
  href: string;     
}

export default function CardInicial({
  sigla,
  descricao,
  icone,
  href,
  className = "",
  ...props
}: CardInicialProps) {
  return (
    <Link href={href} className="block w-full sm:w-64">
      <div
        className={`group relative flex flex-col items-center justify-center p-8 bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl hover:border-cyan-200 transition-all duration-300 hover:-translate-y-2 overflow-hidden cursor-pointer ${className}`}
        {...props}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

        <div className="relative z-10 flex items-center justify-center w-16 h-16 mb-5 rounded-2xl bg-cyan-100 text-cyan-700 group-hover:bg-cyan-600 group-hover:text-white transition-colors duration-300 shadow-sm">
          {icone}
        </div>

        <h3 className="relative z-10 text-2xl font-extrabold text-gray-900 tracking-tight">
          {sigla}
        </h3>
        
        {descricao && (
          <p className="relative z-10 text-sm text-gray-500 text-center mt-2 font-medium">
            {descricao}
          </p>
        )}
      </div>
    </Link>
  );
}