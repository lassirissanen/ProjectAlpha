import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import {
  getTensorflowClassification,
  getCombinedClassification,
  getOpenAIClassification
} from "./backend-service";

jest.mock("./backend-service");

describe("API requests", () => {
  const message = "test message";

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("getTensorflowClassification is working correctly", async () => {
    const response = { classification: "test classification" };
    getTensorflowClassification.mockResolvedValueOnce(response);
    const data = await getTensorflowClassification(message);

    expect(getTensorflowClassification).toHaveBeenCalledWith(message);
    await waitFor(() => expect(data).toEqual(response));
  });

  test("getCombinedClassification is working correctly", async () => {
    const response = { classification: "test classification" };
    getCombinedClassification.mockResolvedValueOnce(response);
    const data = await getCombinedClassification(message);

    expect(getCombinedClassification).toHaveBeenCalledWith(message);
    expect(data).toEqual(response);
  });

  test("getOpenAIClassification", async () => {
    const response = { classification: "test classification" };
    getOpenAIClassification.mockResolvedValueOnce(response);
    const data = await getOpenAIClassification(message);

    expect(getOpenAIClassification).toHaveBeenCalledWith(message);
    expect(data).toEqual(response);
  });
});