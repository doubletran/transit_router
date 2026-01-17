import { useEffect } from "react"
import { LiaWalkingSolid } from "react-icons/lia"
import { IoMdBus } from "react-icons/io"
import { FaMapMarkerAlt } from "react-icons/fa"

export const ResultCard = ({ journey }: ResultCardProps) => {
  useEffect(() => {
    console.log(journey)
  }, [journey])
  const dest = journey[journey.length - 1];
  return (
    <div className="flex justify-center items-center w-full py-4 px-1 border-t-2 border-gray-400">
      <div className="flex flex-col w-full gap-2">
        {journey.map((data, index) => {
          const isFirst = index === 0

          const isWalking = !data.mode || data.mode === "walking"

          // SOURCE CARD
          if (isFirst) {
            return (
              <div key={data.id} className="flex w-full">
                {/* timeline */}
                <div className="flex flex-col items-center mr-3">
                  <div className="w-2 h-2 rounded-full bg-green-600 mt-2" />
                  <div className="flex-1 border-l-2 border-dotted border-gray-300" />
                </div>

                {/* card */}
                <div
                  style={{ backgroundColor: "#F9FAFB", border: "1px solid #E5E7EB" }}
                  className="w-full px-3 py-2 flex justify-between items-center rounded-md"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <FaMapMarkerAlt className="text-green-600 text-lg shrink-0" />
                    <div className="min-w-0">
                      <div className="text-xs text-gray-500 font-medium">Source</div>
                      <div className="text-sm font-semibold text-gray-900 truncate">
                        {data.name}
                      </div>
                    </div>
                  </div>

                  {data.departure_time ? (
                    <span className="text-gray-500 font-mono text-sm ml-3">
                      {data.departure_time}
                    </span>
                  ) : null}
                </div>
              </div>
            )
          }

          // WALK CARD
          if (isWalking) {
            return (
              <div key={data.id} className="flex w-full">
                {/* timeline */}
                <div className="flex flex-col items-center mr-3">
                  <div className="w-2 h-2 rounded-full bg-gray-400 mt-2" />
                  <div className="flex-1 border-l-2 border-dotted border-gray-300" />
                </div>

                {/* content */}
                <div className="w-full px-3 py-2 flex items-center gap-2 text-gray-700">
                  <LiaWalkingSolid className="text-lg shrink-0" />
                  <span className="text-sm font-medium">
                    Walk {data.walking_time}
                  </span>
                </div>
              </div>
            )
          }

          // BUS CARD
          return (
            <div key={data.id} className="flex w-full">
              {/* timeline */}
              <div className="flex flex-col items-center mr-3">
                <div className="w-2 h-2 rounded-full bg-gray-500 mt-2" />
                <div className="flex-1 border-l-2 border-dotted border-gray-300" />
              </div>

              {/* card */}
              <div
                className="w-full px-3 py-2 border-l-4 rounded-md"
                style={{ borderColor: `#${data.color}` }}
              >
                {/* Line 1: Departure (time right) */}
                <div className="flex justify-between text-sm font-medium text-gray-900">
                  <span className="truncate">{journey[index - 1]?.name}</span>
                  <span className="text-gray-500 font-mono ml-3">
                    {data.departure_time}
                  </span>
                </div>

                {/* Line 2: Bus info */}
                <div className="flex items-center gap-2 my-1">
                  <IoMdBus className="text-gray-700 text-lg shrink-0" />
                  <span className="text-sm font-semibold text-gray-800">
                    {data.mode}
                  </span>
                </div>

                {/* Line 3: Arrival (time right) */}
                <div className="flex justify-between text-sm font-medium text-gray-900">
                  <span className="truncate">{data.name}</span>
                  <span className="text-gray-500 font-mono ml-3">
                    {data.arrival_time}
                  </span>
                </div>
              </div>
            </div>
          )
        })}

              <div key={dest.id} className="flex w-full">
                {/* timeline */}
                <div className="flex flex-col items-center mr-3">
                  <div className="w-2 h-2 rounded-full bg-red-600 mt-2" />
                  {/* no line below destination */}
                </div>

                {/* card */}
                <div
                  style={{ backgroundColor: "#F9FAFB", border: "1px solid #E5E7EB" }}
                  className="w-full px-3 py-2 flex justify-between items-center rounded-md"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <FaMapMarkerAlt className="text-red-600 text-lg shrink-0" />
                    <div className="min-w-0">
                      <div className="text-xs text-gray-500 font-medium">Destination</div>
                      <div className="text-sm font-semibold text-gray-900 truncate">
                        {dest.name}
                      </div>
                    </div>
                  </div>

                  <span className="text-gray-500 font-mono text-sm ml-3">
                    {dest.arrival_time}
                  </span>
                </div>
              </div>
            
      </div>
    </div>
  )
}
