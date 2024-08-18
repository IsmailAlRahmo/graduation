import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { QUERY_KEY } from "../constants/queryKeys";
import * as userLocalStorage from "./user.localstore";

async function signIn(data) {
  const response = await fetch("http://127.0.0.1:5001/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Failed on sign up request", response);
  const responseData = await response.json();
  //   console.log(responseData,data);

  return {
    responseData,
    inputData: data,
  };
}

export function useSignIn() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { mutate: signInMutation } = useMutation((data) => signIn(data), {
    onSuccess: (data) => {
      console.log(data);
      queryClient.setQueryData([QUERY_KEY.user], data.inputData);
      userLocalStorage.saveUser(data.inputData);
      navigate("/home/overview");
    },
    onError: (error) => {
      console.log(error);
    },
  });

  return signInMutation;
}
