import { ComponentProps, ReactNode } from "react";
interface ButtonProps extends ComponentProps<"button"> {
  variant?: "primario" | "secundario";
}
export function Button({ variant = "primario", className = "", ...props }: ButtonProps) {
    const baseStyles = "px-8 py-3 rounded-lg font-semibold transition cursor-pointer shadow-sm text-center flex items-center justify-center w-full sm:w-auto";
    const variants = {
    primario: "bg-ciano-vibrante text-white hover:bg-cyan-600",
    secundario: "bg-white text-ciano-vibrante border border-blue-200 hover:bg-blue-50",
  };
    return (
    <button
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    />
  );
}