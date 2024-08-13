import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { QUERY_KEY } from "../constants/queryKeys";

async function signIn(data) {
  const response = await fetch(
    `http://localhost:3000/users/${data.email}`
    //     , {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(data),
    //   }
  );
  if (!response.ok) throw new Error("Failed on sign in request", response);

  return await response.json();
}

export function useSignIn() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { mutate: signInMutation } = useMutation((data) => signIn(data), {
    onSuccess: (data) => {
      console.log(data);
      queryClient.setQueryData([QUERY_KEY.user], data);
      navigate("/home/overview");
    },
    onError: (error) => {
      console.log(error);
    },
  });

  return signInMutation;
}
