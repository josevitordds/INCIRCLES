"use client";

import Link from "next/link";
import Logo from "../components/Logo";
import { Button } from "../components/Button";
import Header from "@/components/Header";
import CardInicial from "@/components/CardInicial";

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen bg-cyan-100">

      <section className="fixed top-0 left-0 w-full z-50">
        <Header />
      </section>
      <section className=" py-16 md:py-24 px-6">
        <div className="max-w-4xl pt-20 mx-auto flex flex-col items-center justify-center gap-8 text-center">
          <div className="flex-1  text-center md:text-center space-y-2">
            <h1 className="text-5xl md:text-5xl font-medium text-gray-900 tracking-tight leading-tight">
              Domine as Olimpíadas Científicas
            </h1>
            <p className="text-lg text-gray-600 max-w-lg mx-auto">
              Acesse milhares de questões da OBMEP, acompanhe seu desempenho no dashboard e aprenda com seus erros. O seu portal definitivo de estudos.
            </p>
            <div className="flex flex-col sm:flex-col gap-4 justify-center items-center md:justify-start pt-20">
              <Link href="/cadastro" className="w-full sm:w-auto">
                <Button variant="primario">
                  Acessar ao sistema de questões
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      <section className="flex-1 bg-white py-16 px-6">
        <div className="max-w-7xl mx-auto flex flex-col items-center">

          <h2 className="text-3xl font-medium text-gray-00 mb-12 text-center">
            Escolha sua Olimpíada
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-5xl justify-items-center">

            <CardInicial
              href="/questoes/obmep"
              sigla="OBMEP"
              descricao="Matemática"
              icone={
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 7V4h16v3" />
                  <path d="M9 4v16" />
                  <path d="M15 4v16" />
                </svg>
              }
            />

            <CardInicial
              href="/questoes/oba"
              sigla="OBA"
              descricao="Astronomia"
              icone={
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2v20" />
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                </svg>
              }
            />

            <CardInicial
              href="/questoes/obf"
              sigla="OBF"
              descricao="Física"
              icone={
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="3" />
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
                </svg>
              }
            />

          </div>
        </div>
      </section>

    </main>
  );
}