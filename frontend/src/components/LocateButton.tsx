import { FaLocationArrow } from 'react-icons/fa6' // Importa el ícono FaLocationArrow desde react-icons
import { useMap } from 'react-leaflet' // Importa el hook useMap de react-leaflet

// Define la interfaz de los props para el componente LocateButton
interface LocateButtonProps {
  setOrigin: (location: [number, number]) => void // Propiedad para establecer la ubicación de origen
}

// Componente LocateButton que acepta los props definidos en LocateButtonProps
export const LocateButton = ({ setOrigin }: LocateButtonProps) => {
  const map = useMap() // Obtiene la instancia del mapa usando el hook useMap

  // Función para manejar la localización del usuario
  const handleLocate = () => {
    if (navigator.geolocation) {
      // Verifica si la geolocalización es soportada por el navegador
      navigator.geolocation.getCurrentPosition(
        position => {
          // Obtiene la posición actual del usuario
          const { latitude, longitude } = position.coords
          map.flyTo([latitude, longitude], 18) // Mueve el mapa a la ubicación actual del usuario con un zoom de 18
          setOrigin([latitude, longitude]) // Establece la ubicación de origen con las coordenadas actuales
        },
        error => {
          // Maneja errores de geolocalización
          console.error('Error getting location: ', error)
        }
      )
    } else {
      // Muestra un error si la geolocalización no es soportada por el navegador
      console.error('Geolocation is not supported by this browser.')
    }
  }

  return (
    <button
      onClick={handleLocate} // Asigna el evento de clic para manejar la localización
      className="absolute bottom-4 right-4 z-[1000] bg-white p-3 rounded-full shadow-lg" // Aplica clases para el estilo del botón
      title="Locate me" // Título del botón
    >
      <FaLocationArrow className="text-blue-500 text-xl" /> {/* Renderiza el ícono FaLocationArrow */}
    </button>
  )
}
