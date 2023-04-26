import { waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import {
  getTensorflowClassification,
  getCombinedClassification,
  getOpenAIClassification
} from "./backend-service";

jest.mock("./backend-service");

describe("API requests", () => {
  const message = "test message";
  const suggestion = "The original suggestion for the appointment";

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("getTensorflowClassification is working correctly", async () => {
    const response = { classification: "test classification" };
    getTensorflowClassification.mockResolvedValueOnce(response);
    const data = await getTensorflowClassification(message, suggestion);

    expect(getTensorflowClassification).toHaveBeenCalledWith(message, suggestion);
    await waitFor(() => expect(data).toEqual(response));
  });

  test("getCombinedClassification is working correctly", async () => {
    const response = { classification: "test classification" };
    getCombinedClassification.mockResolvedValueOnce(response);
    const data = await getCombinedClassification(message, suggestion);

    expect(getCombinedClassification).toHaveBeenCalledWith(message, suggestion);
    expect(data).toEqual(response);
  });

  test("getOpenAIClassification", async () => {
    const response = { classification: "test classification" };
    getOpenAIClassification.mockResolvedValueOnce(response);
    const data = await getOpenAIClassification(message, suggestion);

    expect(getOpenAIClassification).toHaveBeenCalledWith(message, suggestion);
    expect(data).toEqual(response);
  });
});