import { motion } from "framer-motion";

export const Button = ({ children, variant = "primary", className = "", ...props }) => {
  const baseClasses = "relative px-5 py-2.5 font-body font-medium rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-[var(--color-accent-primary)]/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center";
  
  const variants = {
    primary: "bg-[var(--color-accent-primary)] text-white shadow-sm hover:bg-zinc-800",
    secondary: "bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)] text-[var(--color-text-primary)] hover:bg-zinc-100",
    ghost: "bg-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-bg-subtle)]",
    outline: "bg-transparent border border-[var(--color-border-subtle)] text-[var(--color-text-primary)] hover:bg-[var(--color-bg-subtle)]"
  };

  return (
    <motion.button
      whileHover={{ scale: 1.01 }}
      whileTap={{ scale: 0.99 }}
      className={`${baseClasses} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
};
