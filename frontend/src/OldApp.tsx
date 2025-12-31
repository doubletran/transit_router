import { Sidebar } from './components/Sidebar'
import { Map } from './components/Map'
import 'leaflet/dist/leaflet.css'
import { useRef, useState, useEffect } from 'react'
import getRoute from './api/axios'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import {  RouteData } from './components/ResultCard'
import { Feature, Geometry, LineString } from 'geojson'

const colors = ['#F72585', '#7209B7', '#4361EE', '#F033FF', '#FF33F0']; // Colores alternativos para las rutas

function App() {
  // Definir estados para la aplicación
  const [origin, setOrigin] = useState<[number, number] | null>(null) // Estado para el origen
  const [destination, setDestination] = useState<[number, number] | null>(null) // Estado para el destino
  const [routeData, setRouteData] = useState<RouteData[]>([]) // Estado para los datos de la ruta
  const [focusedInput, setFocusedInput] = useState<'origin' | 'destination' | null>(null) // Estado para el input enfocado
  const [selectedRoutes, setSelectedRoutes] = useState<Feature<Geometry>[]>([]) // Estado para las rutas seleccionadas
  const [loading, setLoading] = useState(false) // Estado de carga

  // Crear referencias para los inputs
  const originRef = useRef<HTMLInputElement>(null)
  const destinationRef = useRef<HTMLInputElement>(null)

  // Manejar la obtención de la ruta
  const handleGetRoute = async () => {
    if (origin && destination) {
      setLoading(true) // Iniciar el spinner
      try {
        // Llamar a la API para obtener la ruta
        const data = await getRoute(origin, destination)
        // Formatear los datos obtenidos
        const formattedData: RouteData[] = data.map((item: any) => ({
          properties: {
            bus_number: item.properties.bus_number,
            route: item.properties.route,
            route_class: item.properties.route_class,
            route_type: item.properties.route_type,
            route_1: item.properties.route_1,
            route_1_class: item.properties.route_1_class,
            route_1_type: item.properties.route_1_type,
            route_2: item.properties.route_2,
            route_2_class: item.properties.route_2_class,
            route_2_type: item.properties.route_2_type,
            route_3: item.properties.route_3,
            route_3_class: item.properties.route_3_class,
            route_3_type: item.properties.route_3_type,
            coordinates: item.geometry.coordinates,
          },
          coordinates: item.geometry.coordinates,
        }))
        setRouteData(formattedData) // Actualizar el estado con los datos formateados
        console.log('Route data fetched and formatted:', formattedData)
      } catch (error) {
        console.error('Error fetching route:', error) // Manejar errores
      } finally {
        setLoading(false) // Detener el spinner
      }
    } else {
      toast.error('Por favor, selecciona un origen y un destino') // Mostrar mensaje de error si faltan datos
      console.warn('Both origin and destination must be set')
    }
  }

  // Manejar doble clic en el mapa para establecer origen o destino
  const handleMapDoubleClick = (location: [number, number]) => {
    const [lat, lng] = location
    if (focusedInput === 'origin' && originRef.current) {
      setOrigin(location)
      originRef.current.value = `${lng} ${lat}`
    } else if (focusedInput === 'destination' && destinationRef.current) {
      setDestination(location)
      destinationRef.current.value = `${lng} ${lat}`
    }
  }

  // Manejar la selección de la ruta
  const handleRouteSelect = (coordinates: [number, number][][] | [number, number][]) => {
    setSelectedRoutes([]); // Limpiar las rutas existentes antes de agregar nuevas

    const normalizedCoordinates = Array.isArray(coordinates[0][0]) ? coordinates : [coordinates];

    // Crear características de MultiLineString con colores alternativos
    const multiLineFeatures: Feature<Geometry>[] = normalizedCoordinates.map((line, index) => ({
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: line,
      } as LineString,
      properties: {
        color: colors[index % colors.length], // Alternar colores
      },
    }));
    
    // Establecer rutas seleccionadas después de un pequeño retraso
    setTimeout(() => {
      setSelectedRoutes(multiLineFeatures);
    }, 0); // Retraso para forzar una re-renderización
    
    console.log('Routes selected:', multiLineFeatures);
  };

  // Manejar la limpieza de datos
  const handleClean = () => {
    setOrigin(null);
    setDestination(null);
    setRouteData([]);
    setSelectedRoutes([]);
    if (originRef.current) originRef.current.value = '';
    if (destinationRef.current) destinationRef.current.value = '';
  };

  // Efecto para detectar cambios en las rutas seleccionadas
  useEffect(() => {
    if (selectedRoutes.length > 0) {
      console.log('Selected routes changed:', selectedRoutes);
    }
  }, [selectedRoutes]);

  return (
    <div className="flex h-screen">
      <ToastContainer /> {/* Contenedor para mostrar mensajes toast */}
      <Sidebar
        setFocusedInput={setFocusedInput} // Prop para establecer el input enfocado
        originRef={originRef} // Referencia del input de origen
        destinationRef={destinationRef} // Referencia del input de destino
        onGetRoute={handleGetRoute} // Función para obtener la ruta
        onClean={handleClean} // Función para limpiar los datos
        data={routeData.map(rd => rd.properties)} // Datos de la ruta
        onRouteSelect={handleRouteSelect} // Función para seleccionar la ruta
        loading={loading} // Estado de carga
      />
      <Map
        setOrigin={location => {
          setOrigin(location)
          if (originRef.current) {
            const [lat, lng] = location
            originRef.current.value = `${lng} ${lat}`
          }
        }}
        setDestination={setDestination}
        origin={origin}
        destination={destination}
        onMapDoubleClick={handleMapDoubleClick}
        selectedRoutes={selectedRoutes}
      />
    </div>
  )
}

export default App
