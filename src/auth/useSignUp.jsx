import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { QUERY_KEY } from "../constants/queryKeys";
async function signUp(data) {
    console.log(data);
  const response = await fetch("http://127.0.0.1:5001/register", {
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

export function useSignUp() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const { mutate: signUpMutation } = useMutation((data) => signUp(data), {
    onSuccess: (data) => {
      console.log(data);

      queryClient.setQueryData([QUERY_KEY.user], data.responseData);
      navigate("/signin");
    },
    onError: (error) => {
      console.log(error);
    },
  });

  return signUpMutation;
}
