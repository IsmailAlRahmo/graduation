import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { QUERY_KEY } from '../constants/queryKeys';
async function signUp(data) {
  const response = await fetch("http://localhost:3000/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!response.ok)
    throw new Error("Failed on sign up request", response);

  return await response.json();
}

export function useSignUp() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { mutate: signUpMutation } = useMutation(
    (data) => signUp(data),
    {
      onSuccess: (data) => {
        queryClient.setQueryData([QUERY_KEY.user], data);
        navigate("/signin");
      },
      onError: (error) => {
        console.log(error);
      },
    }
  );

  return signUpMutation;
}
