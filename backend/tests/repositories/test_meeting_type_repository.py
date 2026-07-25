from bson import ObjectId

from app.domain.objects import MeetingTypeObj


class TestCreate:
    async def test_returns_meeting_type_with_id(self, meeting_type_repo):
        result = await meeting_type_repo.create(
            name="Consultation",
            description="30 min meeting",
            duration_minutes=30,
        )

        assert isinstance(result, MeetingTypeObj)
        assert result.id is not None
        assert len(result.id) == 24
        assert result.name == "Consultation"
        assert result.description == "30 min meeting"
        assert result.duration_minutes == 30


class TestFindById:
    async def test_found(self, meeting_type_repo):
        created = await meeting_type_repo.create(
            name="Workshop",
            description="60 min",
            duration_minutes=60,
        )

        found = await meeting_type_repo.find_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.name == "Workshop"
        assert found.duration_minutes == 60

    async def test_not_found(self, meeting_type_repo):
        result = await meeting_type_repo.find_by_id(str(ObjectId()))

        assert result is None


class TestFindAll:
    async def test_empty(self, meeting_type_repo):
        result = await meeting_type_repo.find_all()

        assert result == []

    async def test_returns_all_types(self, meeting_type_repo):
        await meeting_type_repo.create(name="A", description="a", duration_minutes=30)
        await meeting_type_repo.create(name="B", description="b", duration_minutes=60)

        result = await meeting_type_repo.find_all()

        assert len(result) == 2
        names = [t.name for t in result]
        assert "A" in names
        assert "B" in names


class TestFindByIds:
    async def test_returns_subset(self, meeting_type_repo):
        t1 = await meeting_type_repo.create(name="A", description="a", duration_minutes=30)
        t2 = await meeting_type_repo.create(name="B", description="b", duration_minutes=60)
        await meeting_type_repo.create(name="C", description="c", duration_minutes=45)

        result = await meeting_type_repo.find_by_ids([t1.id, t2.id])

        assert len(result) == 2
        ids = [t.id for t in result]
        assert t1.id in ids
        assert t2.id in ids

    async def test_empty_list(self, meeting_type_repo):
        result = await meeting_type_repo.find_by_ids([])

        assert result == []
