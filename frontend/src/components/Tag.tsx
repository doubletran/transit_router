// Componente Tag que acepta un ícono principal, un ícono secundario, un texto y un color opcional
export const Tag = ({
  Icon, // Ícono principal
  Icon2, // Ícono secundario opcional
  Text, // Texto opcional
  Color // Color de fondo opcional
}: {
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>> // Tipo del ícono principal
  Text?: string // Tipo del texto (opcional)
  Color?: string // Tipo del color (opcional)
  Icon2?: React.ComponentType<React.SVGProps<SVGSVGElement>> // Tipo del ícono secundario (opcional)
}) => {
  // Si no se proporciona un color, usar 'bg-amber-500' como color predeterminado
  const color = Color === undefined ? 'bg-amber-500' : Color

  return (
    // Estilo de la etiqueta con el color de fondo y otras clases de estilo
    <div className={`${color} rounded-lg py-1 px-2 flex flex-wrap w-fit items-center justify-center`}>
      {/* Renderizar el ícono principal si está disponible */}
      {Icon && <Icon className="text-white text-2xl " />}
      
      {/* Renderizar el texto si está disponible */}
      {Text === undefined ? null : (
        <p className="text-sm text-white font-bold p-2">{Text}</p>
      )}

      {/* Renderizar el ícono secundario si está disponible */}
      {Icon2 && <Icon2 className="text-white text-md " />} 
    </div>
  )
}
