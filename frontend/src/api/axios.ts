import axios from 'axios';
import { toast } from 'react-toastify';

// Función para calcular la distancia en metros entre dos puntos
const calculateDistance = (point1: [number, number], point2: [number, number]) => {
  const R = 6371e3; // Radio de la Tierra en metros
  const lat1 = point1[0] * (Math.PI / 180); // Convertir latitud del punto 1 a radianes
  const lat2 = point2[0] * (Math.PI / 180); // Convertir latitud del punto 2 a radianes
  const deltaLat = (point2[0] - point1[0]) * (Math.PI / 180); // Diferencia de latitud en radianes
  const deltaLon = (point2[1] - point1[1]) * (Math.PI / 180); // Diferencia de longitud en radianes

  const a =
    Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
    Math.cos(lat1) * Math.cos(lat2) *
    Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2); // Fórmula de Haversine

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); // Fórmula de Haversine

  const distance = R * c; // Calcular la distancia
  return distance;
};

// Función para obtener la ruta entre dos puntos
const getRoute = async (
  origin: [number, number],
  destination: [number, number]
) => {
  const distance = calculateDistance(origin, destination); // Calcular la distancia entre el origen y el destino

  if (distance < 500) {
    toast.warn('Puedes llegar caminando.'); // Mostrar advertencia si la distancia es menor a 500 metros
    return null; // No continuar con la solicitud a la API
  }

  const url = 'http://127.0.0.1:5000/home'; // URL de la API
  const params = {
    point_1: `${origin[1]} ${origin[0]}`, // Latitude Longitude para el punto 1
    point_2: `${destination[1]} ${destination[0]}` // Latitude Longitude para el punto 2
  };

  try {
    console.log('Fetching route...');
    console.log('Origin:', origin);
    console.log('Destination:', destination);

    console.log('point_1:', params.point_1);
    console.log('point_2:', params.point_2);
    const response = await axios.get(url, { params }); // Hacer la solicitud a la API

    // Si response.data es un objeto vacío, lanzar un toast
    if (Object.keys(response.data).length === 0) {
      toast.error(
        'No se encontró una ruta para los puntos seleccionados. Por favor, intenta con otros puntos.'
      );
    }

    return response.data; // Devolver los datos de la respuesta
  } catch (error) {
    console.error('Error fetching route:', error); // Mostrar error en la consola
    throw error; // Lanzar el error
  }
};

export default getRoute;
