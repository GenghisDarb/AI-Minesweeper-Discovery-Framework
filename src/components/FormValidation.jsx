import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Button from "./ui/Button";

const schema = z.object({
  sessionName: z.string().nonempty("Session name is required"),
  dataset: z.string().nonempty("Dataset selection is required"),
});

const FormValidation = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data) => {
    console.log("Form Data:", data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="sessionName" className="block font-medium">
          Session Name
        </label>
        <input
          id="sessionName"
          {...register("sessionName")}
          className="border rounded px-2 py-1 w-full"
        />
        {errors.sessionName && (
          <p className="text-red-500 text-sm">{errors.sessionName.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="dataset" className="block font-medium">
          Dataset
        </label>
        <select
          id="dataset"
          {...register("dataset")}
          className="border rounded px-2 py-1 w-full"
        >
          <option value="">Select a dataset</option>
          <option value="default">Default Dataset</option>
          <option value="custom">Custom Dataset</option>
        </select>
        {errors.dataset && (
          <p className="text-red-500 text-sm">{errors.dataset.message}</p>
        )}
      </div>

      <Button type="submit" variant="default">
        Submit
      </Button>
    </form>
  );
};

export default FormValidation;
