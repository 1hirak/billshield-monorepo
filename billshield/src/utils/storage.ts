const HOUSEHOLD_KEY = "billshield_household_id";
const BILL_KEY = "billshield_bill_id";

export function getHouseholdId(): string | null {
  return localStorage.getItem(HOUSEHOLD_KEY);
}

export function setHouseholdId(id: string) {
  localStorage.setItem(HOUSEHOLD_KEY, id);
}

export function getBillId(): string | null {
  return localStorage.getItem(BILL_KEY);
}

export function setBillId(id: string) {
  localStorage.setItem(BILL_KEY, id);
}

export function removeBillId() {
  localStorage.removeItem(BILL_KEY);
}

export function clearAll() {
  localStorage.removeItem(HOUSEHOLD_KEY);
  localStorage.removeItem(BILL_KEY);
}
