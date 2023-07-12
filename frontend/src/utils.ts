export function handleErrors(response: Response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

export async function patchField(model: string, pk: number, field: string, value: any) {
  await fetch(
    `http://localhost:8000/api/${model}/${pk}/`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        [field]: value,
      }),
    }
  )
    .then(handleErrors)
}
