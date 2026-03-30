"use client";

import Link from "next/link";
import { useState } from "react";
import Logo from "@/components/Logo";
import { Button } from "@/components/Button";
import { Input } from "@/components/InputForm";
import { useRouter } from "next/navigation";

export default function Cadastro() {
  const router = useRouter(); 
  const [erro, setErro] = useState(""); 
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    nome_completo: "",
    email: "",
    senha: "",
    olimpiada_foco: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/auth/cadastro", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        setErro(data.detail || "Erro ao realizar cadastro.");
        setLoading(false);
        return;
      }

      alert("Conta criada com sucesso!");
      router.push("/login");

    } catch (error) {
      setErro("Erro de conexão com o servidor.");
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-cyan-50/50 p-4 md:p-8">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-8 border border-gray-100">

        <div className="flex justify-center mb-6">
          <Logo className="w-auto h-12 text-cyan-800" />
        </div>

        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Crie sua conta</h1>
          <p className="text-gray-500 mt-2 text-sm">Junte-se à plataforma e comece a evoluir</p>
        </div>
        {erro && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 text-sm rounded-lg text-center">
            {erro}
          </div>
        )}

        <form className="space-y-4" onSubmit={handleSubmit}>
          <Input
            label="Nome Completo"
            type="text"
            placeholder="Ex: Machado de Assis"
            required
            value={formData.nome_completo}
            onChange={(e) => setFormData({ ...formData, nome_completo: e.target.value })}
          />

          <Input
            label="E-mail"
            type="email"
            placeholder="seu@email.com"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />

          <Input
            label="Senha"
            type="password"
            placeholder="••••••••"
            required
            minLength={6}
            value={formData.senha}
            onChange={(e) => setFormData({ ...formData, senha: e.target.value })}
          />

          <div className="flex flex-col w-full">
            <label className="mb-1 text-sm font-medium text-gray-700">
              Olimpíada de Foco (Opcional)
            </label>
            <select
              className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none transition shadow-sm bg-white"
              value={formData.olimpiada_foco}
              onChange={(e) => setFormData({ ...formData, olimpiada_foco: e.target.value })}
            >
              <option value="">Selecione uma opção...</option>
              <option value="OBMEP">OBMEP (Matemática)</option>
              <option value="OBA">OBA (Astronomia)</option>
              <option value="OBF">OBF (Física)</option>
            </select>
          </div>

          <Button type="submit" variant="primario" className="w-full mt-4" disabled={loading}>
            {loading ? "Criando conta..." : "Criar Conta"}
          </Button>
        </form>

        <div className="mt-6 flex items-center justify-between">
          <span className="border-b w-1/5 lg:w-1/4"></span>
          <span className="text-xs text-center text-gray-500 uppercase font-medium">Ou continue com</span>
          <span className="border-b w-1/5 lg:w-1/4"></span>
        </div>

        <div className="mt-6">
          <button
            disabled
            className="w-full flex items-center justify-center gap-2 px-8 py-2.5 border border-gray-300 rounded-lg font-semibold bg-gray-50 text-gray-400 cursor-not-allowed transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" className="w-5 h-5 grayscale opacity-50">
              <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z" />
              <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z" />
              <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z" />
              <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z" />
            </svg>
            Google (Em breve)
          </button>
        </div>

        <p className="text-center text-sm text-gray-600 mt-8">
          Já tem uma conta?{" "}
          <Link href="/login" className="text-cyan-700 font-semibold hover:underline">
            Faça login
          </Link>
        </p>

      </div>
    </main>
  );
}