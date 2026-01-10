import { Tag } from "./Tag";
import { LiaWalkingSolid } from "react-icons/lia";
import { FaBusAlt } from "react-icons/fa";
import { IoMdBus } from "react-icons/io";
import { useEffect } from "react";

export interface Trip {
  id: string;
  name: string;
  mode: string;
  color: string;
}

export interface ResultCardProps {
  journey: Trip[];
}

export const ResultCard = ({ journey }: ResultCardProps) => {
  const renderTag = (
    text: string,
    icon: any,
    color?: string,
    icon2?: any
  ) => (
    <Tag Text={text} Icon={icon} Color={color} Icon2={icon2} />
  );
  useEffect(()=>{
    console.log(journey)
  })
  let src = '';

  return (
    <div className="flex justify-center items-center w-full py-4 px-1 border-t-2 border-gray-400">
      <div className="flex flex-wrap gap-2 w-full">
  
        {journey.map((data, index) => {
          if (!data.mode || data.mode == 'walking'){
            return (
              <div key={data.id}>
            {renderTag(
                  `Walk to ${data.name}` ,
                  LiaWalkingSolid
                )}
              </div>
              )
          }
          else{
                 return( 
                  <div key={data.id}>
                    {renderTag(
                    `${data.mode}: ${journey[index-1].name} -> ${data.name}`,
                    IoMdBus,
                    `#${data.color}`
                  )}
                  </div>)
          }


        })}
      </div>
    </div>
  );
};
