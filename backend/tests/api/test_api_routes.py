def test_search_api_items_route(client):
    # Get all without filters
    data = client.get("/api/items").json()
    total = data["total"]
    assert data["page"] == 1
    assert data["pages"] == 1
    assert data["size"] == 20
    assert len(data["items"]) == total

    # Modify pagination params
    data = client.get("/api/items?size=2&page=2").json()
    assert data["total"] == total
    assert data["page"] == 2
    assert data["pages"] == 3
    assert data["size"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["id"] == 3  # Data ordered by id
    assert data["items"][1]["id"] == 4  # Data ordered by id

    # Search by tags (1 tag)
    data = client.get("/api/items?tags=currency").json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["pages"] == 1
    assert data["size"] == 20
    assert len(data["items"]) == 2

    # Search by tags (1 tag) + custom pagination
    data = client.get("/api/items?tags=currency&size=1&page=2").json()
    assert data["total"] == 2
    assert data["page"] == 2
    assert data["pages"] == 2
    assert data["size"] == 1
    assert len(data["items"]) == 1

    # Search by tags (2 tags)
    data = client.get("/api/items?tags=currency,blockchain").json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["pages"] == 1
    assert data["size"] == 20
    assert len(data["items"]) == 1


def test_get_api_item(client):
    # Get an ApiItem
    data = client.get("/api/items/1").json()
    assert data["id"] == 1
    assert data["label"] == "Carbon Intensity API"
    assert data["description"] == "A carbon intensity forecast API"
    assert data["url"] == "https://api.carbonintensity.org.uk"
    assert data["tags"] == ["carbon", "ecology"]


def test_create_edit_delete_api_item(client):
    # Get create new api item
    new_api_item = dict(
        label="A label", description="A description", url="https://www.mydomain.com"
    )
    response = client.post("/api/items", json=new_api_item).json()
    new_id = response["id"]
    assert response["label"] == new_api_item["label"]
    assert response["description"] == new_api_item["description"]
    assert response["url"] == new_api_item["url"]
    assert response["tags"] == []

    # Edit an existing api item
    edited_api_item = dict(description="A brief description")
    response = client.put(f"/api/items/{new_id}", json=edited_api_item).json()
    assert response["id"] == new_id
    assert response["label"] == new_api_item["label"]
    assert response["description"] == edited_api_item["description"]
    assert response["url"] == new_api_item["url"]
    assert response["tags"] == []

    # Delete an existing api item
    response = client.delete(f"/api/items/{new_id}").json()
    assert response == {"message": "success"}
    response = client.get(f"/api/items/{new_id}").json()
    assert response == {"detail": "Item not found"}
