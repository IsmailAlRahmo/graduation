import { Gauge, gaugeClasses, LineChart } from "@mui/x-charts";

import { useUserStats } from "../api/useUserStats";

const Overview = () => {
  const { data, isLoading } = useUserStats();
  console.log({ data });
  const date = new Date();
  const xLabels = ["sesseion 1", "sesseion 2", "sesseion 3"];
  return (
    <div>
      <div className=" w-full pt-6 flex">
        <div className="h-40 w-[834px]  flex justify-between items-center">
          <div className="pl-12 ">
            <h1 className="text-5xl text-slate-200 font-semibold">
              Your overall
              <br />
              score
            </h1>
            <p className="text-sm inline-block mt-5 text-slate-300">
              Monday, 15 July 2024{" "}
            </p>
            <p className="text-sm inline-block pl-4 text-slate-300">
              {date.getHours()}:{date.getMinutes()}
              {date.getHours() < 12 ? " AM" : " PM"}
            </p>
          </div>
          <div className="rounded-3xl bg-[#192533] py-2 w-[250px] h-[170px]">
            <Gauge
              value={!isLoading ? data[0].oa : 0}
              valueMax={5}
              className=" w-[250px] h-[130px]"
              innerRadius="75%"
              outerRadius="100%"
              sx={{
                [`& .${gaugeClasses.valueText}`]: {
                  fontSize: 18,
                  stroke: "#FFFFFF",
                  transform: "translate(0px, 0px)",
                },
                [`& .${gaugeClasses.referenceArc}`]: {
                  fill: "#FFFFFF",
                },
              }}
              text={({ value, valueMax }) => `${value} / ${valueMax}`}
            />
            <p className="text-center text-slate-200">NICE SHOW!</p>
          </div>
        </div>

        <div className="font-bold w-[250px] h-[160px] bg-[#dadee2] rounded-3xl ml-5">
          <p className="text-sm ml-4 pt-2">Body language score:</p>
          <Gauge
            value={!isLoading ? data[0].bl : 0}
            valueMax={5}
            className="w-[250px] h-[130px]"
            innerRadius="75%"
            outerRadius="100%"
            sx={{
              [`& .${gaugeClasses.valueText}`]: {
                fontSize: 18,
                transform: "translate(0px, 0px)",
              },
              [`& .${gaugeClasses.referenceArc}`]: {
                fill: "#FFFFFF",
              },
            }}
            text={({ value, valueMax }) => `${value} / ${valueMax}`}
          />
        </div>
      </div>
      <div className="w-full h-[326px] flex">
        <div className=" h-full w-[834px] pb-1 pt-3">
          <div className="rounded-3xl bg-[#192533] pb-16 w-full h-full">
            <h1 className="text-center pt-5 text-slate-300">
              Your trend chart
            </h1>

            <LineChart
              className="w-full h-full"
              grid={{ horizontal: true }}
              xAxis={[{ scaleType: "point", data: xLabels }]}
              series={[{ type: "line", data: [1.2, 4.4, 2.5] }]}
              sx={{
                "& .MuiChartsAxis-left .MuiChartsAxis-line": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-left .MuiChartsAxis-tick": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-left": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom .MuiChartsAxis-line ": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom .MuiChartsAxis-tick": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsAxis-bottom": {
                  stroke: "#94a3b8",
                },
                "& .MuiChartsGrid-line": {
                  stroke: "#94a3b8",
                },
              }}
            />
          </div>
        </div>
        <div className=" pl-4 pt-3">
          <div className=" rounded-3xl bg-[#192533] mx-auto">
            <h1 className=" text-sm ml-4 pt-2 text-slate-200">
              Facial expressions score:
            </h1>
            <div className="">
              <Gauge
                value={!isLoading ? data[0].fe : 0}
                valueMax={5}
                className=" w-[250px] h-[120px]"
                innerRadius="75%"
                outerRadius="100%"
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 18,
                    stroke: "#FFFFFF",
                    transform: "translate(0px, 0px)",
                  },
                  [`& .${gaugeClasses.referenceArc}`]: {
                    fill: "#FFFFFF",
                  },
                }}
                text={({ value, valueMax }) => `${value} / ${valueMax}`}
              />
            </div>
          </div>
          <div className="bg-[#dadee2] rounded-3xl text-sm mt-3">
            <h1 className=" text-sm ml-4 pt-2">Vocal tone score:</h1>
            <div className="font-bold mx-auto">
              <Gauge
                value={!isLoading ? data[0].vt : 0}
                valueMax={5}
                className="w-[250px] h-[120px]"
                innerRadius="75%"
                outerRadius="100%"
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 18,
                    transform: "translate(0px, 0px)",
                  },
                  [`& .${gaugeClasses.referenceArc}`]: {
                    fill: "#FFFFFF",
                  },
                }}
                text={({ value, valueMax }) => `${value} / ${valueMax}`}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
