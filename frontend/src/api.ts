export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// Auth functions
export async function signup(email: string, password: string) {
	const res = await fetch(`${API_BASE}/api/v1/auth/signup`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ email, password }),
	});
	if (!res.ok) throw new Error("signup failed");
	return res.json();
}

export async function login(email: string, password: string) {
	const formData = new FormData();
	formData.append("username", email);
	formData.append("password", password);
	
	const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
		method: "POST",
		body: formData,
	});
	if (!res.ok) throw new Error("login failed");
	return res.json();
}

export async function getCurrentUser(token: string) {
	const res = await fetch(`${API_BASE}/api/v1/auth/me`, {
		headers: { Authorization: `Bearer ${token}` },
	});
	if (!res.ok) throw new Error("get user failed");
	return res.json();
}

// Project functions
export async function createProject(title: string, token: string) {
	const res = await fetch(`${API_BASE}/api/v1/projects`, {
		method: "POST",
		headers: { 
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ title }),
	});
	if (!res.ok) throw new Error("create project failed");
	return res.json();
}

export async function getProjects(token: string) {
	const res = await fetch(`${API_BASE}/api/v1/projects`, {
		headers: { Authorization: `Bearer ${token}` },
	});
	if (!res.ok) throw new Error("get projects failed");
	return res.json();
}

export async function getProject(projectId: number, token: string) {
	const res = await fetch(`${API_BASE}/api/v1/projects/${projectId}`, {
		headers: { Authorization: `Bearer ${token}` },
	});
	if (!res.ok) throw new Error("get project failed");
	return res.json();
}

// Image functions
export async function uploadImage(file: File, projectId?: number, token?: string) {
	const form = new FormData();
	form.append("file", file);
	if (projectId) {
		form.append("project_id", projectId.toString());
	}
	
	const headers: Record<string, string> = {};
	if (token) {
		headers.Authorization = `Bearer ${token}`;
	}
	
	const res = await fetch(`${API_BASE}/api/v1/images`, { 
		method: "POST", 
		body: form,
		headers
	});
	if (!res.ok) throw new Error("upload failed");
	return res.json();
}

export async function segment(image_path: string, token?: string) {
	const headers: Record<string, string> = { "Content-Type": "application/json" };
	if (token) {
		headers.Authorization = `Bearer ${token}`;
	}
	
	const res = await fetch(`${API_BASE}/api/v1/ops/segment`, {
		method: "POST",
		headers,
		body: JSON.stringify({ image_path }),
	});
	if (!res.ok) throw new Error("segment failed");
	return res.json();
}

export async function recolor(image_path: string, mask_path: string, dh = 0, ds = 0, dv = 0, token?: string) {
	const headers: Record<string, string> = { "Content-Type": "application/json" };
	if (token) {
		headers.Authorization = `Bearer ${token}`;
	}
	
	const res = await fetch(`${API_BASE}/api/v1/ops/recolor`, {
		method: "POST",
		headers,
		body: JSON.stringify({ image_path, mask_path, dh, ds, dv }),
	});
	if (!res.ok) throw new Error("recolor failed");
	return res.json();
}

export async function overlayWheel(baseImagePath: string, wheelImagePath: string, points: Array<{x: number, y: number}>, token?: string) {
	const headers: Record<string, string> = { "Content-Type": "application/json" };
	if (token) {
		headers.Authorization = `Bearer ${token}`;
	}
	
	const res = await fetch(`${API_BASE}/api/v1/ops/overlay/wheel`, {
		method: "POST",
		headers,
		body: JSON.stringify({ 
			base_image_path: baseImagePath, 
			wheel_image_path: wheelImagePath, 
			dst_pts: points 
		}),
	});
	if (!res.ok) throw new Error("overlay wheel failed");
	return res.json();
}

// Catalog functions
export async function getWheels(brand?: string) {
	const params = new URLSearchParams();
	if (brand) params.append("brand", brand);
	
	const res = await fetch(`${API_BASE}/api/v1/catalog/wheels?${params}`);
	if (!res.ok) throw new Error("get wheels failed");
	return res.json();
}

export async function getVehicleSpecs(make?: string, model?: string, year?: number) {
	const params = new URLSearchParams();
	if (make) params.append("make", make);
	if (model) params.append("model", model);
	if (year) params.append("year", year.toString());
	
	const res = await fetch(`${API_BASE}/api/v1/catalog/vehicles?${params}`);
	if (!res.ok) throw new Error("get vehicle specs failed");
	return res.json();
}

// Share functions
export async function shareProject(projectId: number, token: string) {
	const res = await fetch(`${API_BASE}/api/v1/share/projects`, {
		method: "POST",
		headers: { 
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ project_id: projectId }),
	});
	if (!res.ok) throw new Error("share project failed");
	return res.json();
}


