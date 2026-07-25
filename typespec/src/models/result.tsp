model Success<T> {
  type: "success";
  data: T;
}

model Failure {
  type: "failure";
  error: string;
  code: string;
}

alias Result<T> = Success<T> | Failure;
