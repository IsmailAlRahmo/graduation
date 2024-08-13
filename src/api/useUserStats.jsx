import { useQuery } from "react-query";

async function fetchUserStats() {
  const response = await fetch(`http://localhost:3000/stats`);
  if (!response.ok) throw new Error("Failed on get user request", response);

  return await response.json();
}

export const useUserStats = () => {
  const {
    data,
    isLoading,
    isFetching,
  } = useQuery(["stats"], fetchUserStats, {
    refetchOnWindowFocus: false,
    retry: 2,
  });

  return {
    data,
    isLoading,
    isFetching,
  };
};
