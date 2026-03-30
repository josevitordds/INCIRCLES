'use client'
import Link from "next/link";
import Logo, { LogoPrimary } from "./Logo";
import { Button } from "./Button";

export default function Header() {
    return (
        <div className="w-full bg-white shadow-md p-4 flex items-center justify-between">
            <LogoPrimary className="w-auto h-auto" />
            <nav className="space-x-5 flex items-center justify-center">
                <Link href="/central-de-ajuda" className="text-gray-300 hover:text-gray-400 font-medium">
                    Central de ajuda
                </Link>
                <Link href="/cadastro" className="w-full sm:w-auto">
                    <Button variant="secundario">
                        Começar Agora
                    </Button>
                </Link>
                <Link href="/login" className="w-full sm:w-auto">
                    <Button variant="primario">
                        Entrar
                    </Button>
                </Link>
            </nav>
        </div>
    )

}