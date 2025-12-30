import { ReactNode } from "react"

// Define la interfaz de los props para el componente Button
interface ButtonProps {
  onClick: () => void // Propiedad para manejar el evento de clic
  text: string | ReactNode // Propiedad para el texto o contenido del botón
  color: string  // Propiedad para el color del botón
}

// Componente Button que acepta los props definidos en ButtonProps
export const Button = (props: ButtonProps) => {
  return (
    <button
      onClick={props.onClick} // Asigna el evento de clic al botón
      className={`${props.color} text-white font-bold text-sm py-2 px-4 w-fit rounded-lg`}
      // Agrega clases para el estilo del botón, incluyendo el color, texto blanco, negrita, tamaño de texto, padding, ancho y bordes redondeados
    >
      {props.text} 
    </button>
  )
}
