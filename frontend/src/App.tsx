import { Sidebar } from './components/Sidebar'
import { Map } from './components/Map'
import 'leaflet/dist/leaflet.css'

import { useRef, useState, useEffect } from 'react'
import getRoute from './api/axios'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import {  Trip } from './components/ResultCard'
import { Feature, Geometry, LineString } from 'geojson'
import axios from 'axios'


const colors = ['#F72585', '#7209B7', '#4361EE', '#F033FF', '#FF33F0']; // Colores alternativos para las rutas
const API_URL = 'http://127.0.0.1:5000/'
function App() {
  // Definir estados para la aplicación
  const [origin, setOrigin] = useState<[number, number] | null>(null) // Estado para el origen
  const [destination, setDestination] = useState<[number, number] | null>(null) // Estado para el destino
  const [journey, setJourney] = useState<Trip[]>([]) // Estado para los datos de la ruta
  const [focusedInput, setFocusedInput] = useState<'origin' | 'destination' | null>(null) // Estado para el input enfocado
  const [selectedRoutes, setSelectedRoutes] = useState<Feature<Geometry>[]>([]) // Estado para las rutas seleccionadas
  const [loading, setLoading] = useState(true) // Estado de carga
  const [stops, setStops] = useState<Feature<Geometry>[]>([])
   const [error, setError] = useState(null)
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
       let routes = []
       let _journey = []
        setSelectedRoutes(data.routes)
        setStops(data.stops)
        for (const stop of data.stops){
          _journey.push(stop['properties'])
        }
        setJourney(_journey)
       //setSelectedRoutes(data.geometry)
        console.log('Route data fetched and formatted:',data)
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
  }

  // Efecto para detectar cambios en las rutas seleccionadas
  useEffect(() => {
    if (selectedRoutes.length > 0) {
      console.log('Selected routes changed:', selectedRoutes);
    }
    const getAllStops = async() =>{
    try {
      setLoading(true);
      const response = await axios.get<Stop[]>(`${API_URL}/stops`);
      console.log('Stop data', response.data[0][0])
      setStops(response.data[0][0]);
      setError(null);
    } catch (err) {
      setError(err.message);
      setStops(null);
    } };
    const init = async()=>{
      try{
          setLoading(true)
          const response = await axios.get(`${API_URL}/route/NBUS`);
          console.log(response)
          setSelectedRoutes([response.data])
          setError(null);
      } catch (err) {
      setError(err.message);

    } };
      
    //getAllStops();
    //init()
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
        data={journey} // Datos de la ruta
      //  onRouteSelect={handleRouteSelect} // Función para seleccionar la ruta
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
        stops={stops}
      />
    </div>
  )
}

export default App
