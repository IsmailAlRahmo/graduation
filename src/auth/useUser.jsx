import { useQuery } from "react-query";
import { QUERY_KEY } from "../constants/queryKeys";
import { useEffect } from "react";
import * as userLocalStorage from "./user.localstore";

async function getUser(user) {
  if (!user) return null;
  //   const response = await fetch(`http://localhost:3000/users/${user.email}`);
  //   if (!response.ok) throw new Error("Failed on get user request", response);

  //   return await response.json();
  console.log("local user", userLocalStorage.getUser);

  return userLocalStorage.getUser;
}

export function useUser() {
  // console.log(inputUser);

  const { data: user } = useQuery([QUERY_KEY.user], async () => getUser(user), {
    refetchOnMount: false,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    initialData: userLocalStorage.getUser,
    onError: () => {
      userLocalStorage.removeUser();
    },
  });

  useEffect(() => {
    if (!user) userLocalStorage.removeUser();
    else userLocalStorage.saveUser(user);
  }, [user]);

  return {
    user: user ?? null,
  };
}
