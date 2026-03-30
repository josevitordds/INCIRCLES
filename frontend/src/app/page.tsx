'use cliente';

import Link from "next/link";
import Logo from "../components/Logo";
import { Button } from "../components/Button";
import './globals.css';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-page-light p-6">
      <div className="max-w-3xl text-center space-y-8">
        <div className="flex justify-center mb-6">
          <Logo className="w-auto h-auto" />
        </div>
        <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight">
          Domine as Olimpíadas Científicas
        </h1>
        <p className="text-xl text-gray-600">
          Acesse milhares de questões da OBMEP, acompanhe seu desempenho no dashboard e aprenda com seus erros. O seu portal definitivo de estudos.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
          <Link href="/cadastro" className="w-full sm:w-auto">
            <Button variant="primario">
              Começar Agora
            </Button>
          </Link>
          <Link href="/login" className="w-full sm:w-auto">
            <Button variant="secundario">
              Já tenho uma conta
            </Button>
          </Link>
        </div>
      </div>
    </main>
  );
}