import { describe, it, expect, beforeEach } from "vitest";
import {
  getHouseholdId,
  setHouseholdId,
  getBillId,
  setBillId,
  removeBillId,
  clearAll,
} from "@/utils/storage";

describe("storage", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe("householdId", () => {
    it("returns null when not set", () => {
      expect(getHouseholdId()).toBeNull();
    });

    it("sets and gets value", () => {
      setHouseholdId("abc-123");
      expect(getHouseholdId()).toBe("abc-123");
    });

    it("overwrites previous value", () => {
      setHouseholdId("first");
      setHouseholdId("second");
      expect(getHouseholdId()).toBe("second");
    });
  });

  describe("billId", () => {
    it("returns null when not set", () => {
      expect(getBillId()).toBeNull();
    });

    it("sets and gets value", () => {
      setBillId("bill-456");
      expect(getBillId()).toBe("bill-456");
    });

    it("removes bill id", () => {
      setBillId("bill-456");
      removeBillId();
      expect(getBillId()).toBeNull();
    });
  });

  describe("clearAll", () => {
    it("clears both household and bill", () => {
      setHouseholdId("h-1");
      setBillId("b-1");
      clearAll();
      expect(getHouseholdId()).toBeNull();
      expect(getBillId()).toBeNull();
    });
  });

  describe("independence", () => {
    it("household and bill IDs are stored independently", () => {
      setHouseholdId("h-only");
      expect(getHouseholdId()).toBe("h-only");
      expect(getBillId()).toBeNull();
    });
  });
});
