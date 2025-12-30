// Define la interfaz de los props para el componente Input
interface InputProps {
  text: string // Propiedad para el texto del placeholder
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>> // Propiedad para el ícono del input
  inputRef: React.Ref<HTMLInputElement> // Propiedad para la referencia del input
  onFocus: () => void // Propiedad para manejar el evento de foco
}

// Componente Input que acepta los props definidos en InputProps
export const Input = ({ text, Icon, inputRef, onFocus }: InputProps) => {
  return (
    <div className="relative flex items-center">
      {Icon && <Icon className="absolute left-2.5 text-black" />}
      {/* Renderiza el ícono si está definido */}
      <input
        type="text"
        className="w-full border-2 border-gray-300 rounded-xl pl-8 pr-2 py-2"
        // Aplica clases para el estilo del input, incluyendo borde, redondeo, padding y ancho completo
        placeholder={text} // Asigna el texto del placeholder
        ref={inputRef} // Asigna la referencia del input
        onFocus={onFocus} // Asigna el evento de foco al input
      />
    </div>
  )
}
